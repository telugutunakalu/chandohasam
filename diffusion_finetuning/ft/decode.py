"""Stage 3 decoder (PLAN §6): metre-constrained, left-to-right sequential Monte Carlo.

    uv run --project ../diffusion_pretraining python -m ft.decode --run runs/s2-... \\
        --metre utpalamala --meaning "..." [--particles 16 --guidance 1.5]

The condition (metre, register, meaning) is fixed as in a T1 canvas; the poem is written one
token per step, left to right, into the masked region after it. At each step every particle's
next-token distribution is the model's, restricted by the metre (hard), shifted by the yati
and word-lexicon penalties (soft), and optionally sharpened by classifier-free guidance with
the T0 canvas (empty meaning). Particles carry importance weights (the probability mass their
constraints kept) and are resampled when the effective sample size drops. Finished poems are
checked by the engines and reranked by the model's own poem -> meaning likelihood (T2).
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

from mdlm.diffusion import invalid_bias
from mdlm.model import Denoiser, ModelConfig

from . import DATA_DIR
from .canvas import Vocab, canvas_T2, tokenise_record
from .constraints import Constraint, build_token_table, poem_budget
from .lexicon import LexiconScorer, Trie
from .loss import role_nelbo
from .metres import catalogue_label
from .text import CLASSICAL, MEANING_KEY, METRE_KEY, POEM_KEY, SRC_EDITION, STYLE_KEY, clean_meaning
from .yati_oracle import YatiOracle


def replace_done(st):
    """A finished (or dead) particle: only <eos> is allowed; its row is ignored anyway."""
    return dataclasses.replace(st, done=True)


@dataclass
class DecodeConfig:
    particles: int = 16
    temperature: float = 1.0
    guidance: float = 0.0          # classifier-free guidance weight (0 = off)
    lexicon_lam: float = 2.0       # penalty for a syllable that continues no lexicon word (0 = off)
    lexicon_lam2: float = 0.5      # penalty for starting a new word without a space (compound)
    yati_weight: float = 3.0       # penalty for a non-maitri syllable at a yati (0 = off; large = hard)
    yati_profile: str = "relaxed"  # the yati engine profile of the maitri verdict (PLAN §6.4: constraints relaxed)
    yati_sandhi: str = "hypothesis"  # the yati engine's sandhi mode (off / hypothesis / acchu)
    prasa_relaxed: bool = True     # prāsa keys use the relaxed equivalences (శ~స, ణ~న, ళ~ల, ఱ~ర, ధ~థ)
    vikalpa: bool = True           # pending weights admit the vikalpa readings (False: canonical scansion)
    ess_threshold: float = 0.5     # resample when ESS < threshold * particles
    canvas: int = 512
    rerank: bool = True
    constrained: bool = True       # False: the same sampler with only the model (a baseline)
    seed: int = 0


def metre_header(label: str) -> str:
    return "+".join(catalogue_label(m) or m for m in label.split("+"))


def load_model(run: Path, device) -> tuple[Denoiser, dict]:
    """EMA weights of a run directory (newest checkpoint), a snapshot or a model file."""
    from .train import load_init
    sd, cfg, prov = load_init(str(run))
    model = Denoiser(ModelConfig(**cfg)).to(device).eval()
    model.load_state_dict(sd)
    return model, prov


class Decoder:
    def __init__(self, model: Denoiser, tok, device, cfg: DecodeConfig, data_dir: Path = DATA_DIR):
        self.model, self.tok, self.device, self.cfg = model, tok, device, cfg
        self.v = Vocab(tok)
        self.tt = build_token_table(tok, prasa_relaxed=cfg.prasa_relaxed)
        self.yati = YatiOracle(tok, self.tt, cfg.yati_profile, cfg.yati_sandhi, cache_dir=data_dir / "yati_oracle") \
            if cfg.yati_weight > 0 else None
        self._yati_rows: dict = {}
        self._pollu_masks: dict = {}
        trie_path = data_dir / "lexicon" / "trie.npz"
        self.lex = LexiconScorer(Trie.load(trie_path), self.tt, cfg.lexicon_lam, cfg.lexicon_lam2) \
            if cfg.lexicon_lam > 0 and trie_path.exists() else None
        self.mask_id = tok.special_to_id["<mask>"]
        mc = model.cfg
        self.bias = invalid_bias(mc.padded_vocab, tok.vocab_size, [self.mask_id, tok.pad_id, tok.unk_id], device)
        self.V = tok.vocab_size
        t = lambda a, dt=None: torch.as_tensor(a, device=device, dtype=dt)
        self.g_syl = t(self.tt.is_syl)
        self.g_cls = t(self.tt.cls.astype(np.int64))
        self.g_prasa = t(self.tt.prasa_key.astype(np.int64))
        self.g_bindu = t(self.tt.bindu)
        self.g_vowel = t(self.tt.vowel_onset)
        if self.lex is not None:
            self.g_root = t(self.lex.root_toks.astype(np.int64))

    def _masks(self, specs: list, words: list, todo: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Hard masks and soft penalties for all particles at once (K, V)."""
        K, V, dev, tt = len(specs), self.V, self.device, self.tt
        ok = torch.as_tensor(np.stack([s.ok_cls for s in specs]), device=dev)                 # (K, 6)
        hard = ok.gather(1, self.g_cls.expand(K, V)) & self.g_syl
        prasa = torch.as_tensor([s.prasa for s in specs], device=dev)
        rows = prasa >= 0
        if rows.any():
            hard[rows] &= (self.g_prasa[None] == prasa[rows, None]) | ~self.g_syl
        block = torch.as_tensor([s.block for s in specs], device=dev)
        if block.any():
            hard[block] &= ~self.g_syl
        bindu = torch.as_tensor([s.bindu for s in specs], device=dev)
        rows = bindu >= 0
        if rows.any():
            hard[rows] &= (self.g_bindu[None] == (bindu[rows, None] > 0)) | ~self.g_syl
        for col, flag in ((tt.space, "space"), (tt.newline, "nl"), (tt.eos, "eos")):
            hard[:, col] = torch.as_tensor([getattr(s, flag) for s in specs], device=dev)
        vowel = torch.as_tensor([s.no_vowel for s in specs], device=dev)
        if vowel.any():
            hard[vowel] &= ~self.g_vowel
        for k, s in enumerate(specs):
            if s.pollu_ok is not None and todo[k]:
                hard[k] &= self._pollu_mask(s.pollu_ok) | ~self.g_syl
        soft = torch.zeros((K, V), device=dev)
        if self.yati is not None:
            for k, s in enumerate(specs):
                if s.yati is not None and todo[k]:
                    soft[k] = -self.cfg.yati_weight * (~self._yati_row(s.yati) & self.g_syl).float()
        if self.lex is not None:
            lam, lam2 = self.lex.lam, self.lex.lam2
            for k in range(K):
                if not todo[k]:
                    continue
                node = words[k]
                row = torch.where(self.g_syl, torch.tensor(-lam, device=dev), torch.tensor(0.0, device=dev))
                if node >= 0:
                    toks, _ = self.lex.trie.children(node)
                    if node != 0 and self.lex.trie.terminal[node]:
                        row[self.g_root] = -lam2
                    row[torch.as_tensor(toks.astype(np.int64), device=dev)] = 0.0
                    end = node == 0 or bool(self.lex.trie.terminal[node])
                    row[[tt.space, tt.newline, tt.eos]] = 0.0 if end else -lam
                else:
                    row[[tt.space, tt.newline, tt.eos]] = 0.0
                soft[k] += row
        return hard, soft

    def _pollu_mask(self, ok: frozenset) -> torch.Tensor:
        m = self._pollu_masks.get(ok)
        if m is None:
            m = torch.as_tensor(np.isin(self.tt.pollu, list(ok)), device=self.device)
            self._pollu_masks[ok] = m
        return m

    def _yati_row(self, req: tuple) -> torch.Tensor:
        row = self._yati_rows.get(req)
        if row is None:
            row = torch.as_tensor(self.yati.row(*req), device=self.device)
            self._yati_rows[req] = row
        return row

    def save_yati_cache(self) -> None:
        """Keep the yati readings and pair verdicts computed so far (data/yati_oracle/)."""
        if self.yati is not None:
            self.yati.save()

    # ---- prompts -------------------------------------------------------------------------
    def prefix(self, label: str, meaning: str, register: str = CLASSICAL, src: str = SRC_EDITION,
               empty: bool = False) -> list[int]:
        head = f"{METRE_KEY}: {metre_header(label)}\n{STYLE_KEY}: {register}\n"
        head += f"{MEANING_KEY}:\n" if empty else f"{MEANING_KEY} ({src}): {clean_meaning(meaning)}\n"
        return [self.tok.bos_id] + self.tok.encode(head + f"{POEM_KEY}:\n")

    # ---- the sampler ------------------------------------------------------------------------
    @torch.no_grad()
    def generate(self, label: str, meaning: str, register: str = CLASSICAL, src: str = SRC_EDITION) -> dict:
        cfg, dev, K, V = self.cfg, self.device, self.cfg.particles, self.V
        g = torch.Generator(dev).manual_seed(cfg.seed)
        pre = self.prefix(label, meaning, register, src)
        budget = min(poem_budget(label), cfg.canvas - len(pre) - 1)
        if budget < 32:
            raise ValueError(f"meaning too long for the canvas ({len(pre)} tokens)")
        L = len(pre) + budget + 1
        canv = torch.full((K, L), self.mask_id, dtype=torch.long, device=dev)
        canv[:, : len(pre)] = torch.tensor(pre, device=dev)
        ucanv, upre = None, None
        if cfg.guidance:
            upre = self.prefix(label, "", register, src, empty=True)
            ucanv = torch.full((K, len(upre) + budget + 1), self.mask_id, dtype=torch.long, device=dev)
            ucanv[:, : len(upre)] = torch.tensor(upre, device=dev)
        con = Constraint(label, self.tt, self.yati, vikalpa=cfg.vikalpa) if cfg.constrained else None
        states = [con.initial() if con else None] * K
        words = [0] * K
        logw = torch.zeros(K, device=dev, dtype=torch.float64)
        alive = torch.ones(K, dtype=torch.bool, device=dev)
        done = torch.zeros(K, dtype=torch.bool, device=dev)
        n_resample = 0
        kept_mass = []
        for pos in range(budget):
            todo = alive & ~done
            if not todo.any():
                break
            p = len(pre) + pos
            with torch.autocast(dev.type, dtype=torch.bfloat16, enabled=dev.type == "cuda"):
                logits = self.model.logits(self.model.hidden(canv)[:, p]).float()
                if ucanv is not None:
                    lu = self.model.logits(self.model.hidden(ucanv)[:, len(upre) + pos]).float()
                    logits = lu + cfg.guidance * (logits - lu)
            logp = torch.log_softmax(logits / cfg.temperature + self.bias, dim=-1)[:, :V]
            if con is not None:
                specs = [con.spec(states[k]) if todo[k] else con.spec(replace_done(states[k])) for k in range(K)]
                hard, soft = self._masks(specs, words, todo)
            else:
                hard = torch.ones((K, V), dtype=torch.bool, device=dev)
                soft = torch.zeros((K, V), device=dev)
            score = torch.where(hard, logp + soft, torch.full_like(logp, -math.inf))
            logz = torch.logsumexp(score, dim=-1)
            dead = todo & ~torch.isfinite(logz)
            alive &= ~dead
            logw[dead] = -math.inf
            u = torch.rand(score.shape, device=dev, generator=g).clamp_(1e-20, 1.0)
            nxt = (score - torch.log(-torch.log(u))).argmax(-1)
            with torch.no_grad():
                kept_mass.append(float(torch.exp(torch.logsumexp(torch.where(hard, logp, torch.full_like(logp, -math.inf)),
                                                                 -1))[todo & alive].mean()) if (todo & alive).any() else 0.0)
            for k in range(K):
                if not (todo[k] and alive[k]):
                    continue
                t = int(nxt[k])
                logw[k] += float(logz[k])
                canv[k, p] = t
                if ucanv is not None:
                    ucanv[k, len(upre) + pos] = t
                if con is not None:
                    states[k] = con.advance(states[k], t)
                if self.lex is not None:
                    words[k] = self.lex.advance(words[k], t)
                if t == self.tok.eos_id:
                    done[k] = True
                    canv[k, p:] = self.tok.eos_id
                    if ucanv is not None:
                        ucanv[k, len(upre) + pos:] = self.tok.eos_id
            live = alive & (logw > -math.inf)
            if live.sum() > 1:
                w = torch.exp(logw[live] - logw[live].max())
                ess = float(w.sum() ** 2 / (w ** 2).sum())
                if ess < cfg.ess_threshold * int(live.sum()):
                    idx = torch.nonzero(live).squeeze(1)
                    pick = idx[self._systematic(w / w.sum(), K, g)]
                    canv = canv[pick].clone()
                    if ucanv is not None:
                        ucanv = ucanv[pick].clone()
                    states = [states[int(i)] for i in pick]
                    words = [words[int(i)] for i in pick]
                    done = done[pick].clone()
                    alive = torch.ones(K, dtype=torch.bool, device=dev)
                    mean = torch.logsumexp(logw[live], 0) - math.log(int(live.sum()))
                    logw = torch.full((K,), float(mean), device=dev, dtype=torch.float64)
                    n_resample += 1
        cands = {}
        for k in range(K):
            if not (done[k] and alive[k]):
                continue
            ids = canv[k, len(pre):].tolist()
            ids = ids[: ids.index(self.tok.eos_id)] if self.tok.eos_id in ids else ids
            text = self.tok.decode(ids)
            if text not in cands or float(logw[k]) > cands[text]["logw"]:
                cands[text] = {"poem": text, "lines": [ln.strip() for ln in text.split("\n") if ln.strip()],
                               "logw": float(logw[k])}
        out = {"metre": label, "candidates": list(cands.values()), "resamples": n_resample,
               "allowed_mass": float(np.mean(kept_mass)) if kept_mass else None}
        if cfg.rerank and out["candidates"]:
            self.rerank(out, label, meaning, register, src)
        return out

    @staticmethod
    def _systematic(p: torch.Tensor, n: int, g: torch.Generator) -> torch.Tensor:
        u = (torch.rand((), device=p.device, generator=g) + torch.arange(n, device=p.device)) / n
        return torch.searchsorted(torch.cumsum(p, 0), u.to(p.dtype)).clamp(max=len(p) - 1)

    # ---- rerank ---------------------------------------------------------------------------
    @torch.no_grad()
    def reverse_nll(self, label: str, lines: list[str], meaning: str, register: str, src: str) -> float:
        """Model NELBO of the meaning given the poem (T2 canvas), per meaning token, over fixed masks."""
        rec = {"id": "q", "status": "agree", "meter": label.split("+")[0], "meter_te": metre_header(label),
               "register": register, "lines": lines, "meaning": clean_meaning(meaning), "meaning_src": src,
               "glosses": [], "samasya": None}
        c = canvas_T2(self.v, tokenise_record(self.v, rec))
        if c is None:
            return float("inf")
        x = torch.from_numpy(c[0]).to(self.device).unsqueeze(0).repeat(6, 1)
        roles = torch.from_numpy(c[1]).to(self.device).unsqueeze(0).repeat(6, 1)
        t = torch.tensor([0.2, 0.35, 0.5, 0.65, 0.8, 0.95], device=self.device)
        with torch.autocast(self.device.type, dtype=torch.bfloat16, enabled=self.device.type == "cuda"):
            r = role_nelbo(self.model, x, roles, self.mask_id, self.bias, t=t,
                           generator=torch.Generator(self.device).manual_seed(11))
        keep = ~r["fill"]
        return float((r["ce"][keep] / r["t"][keep]).sum()) / max(1, r["n_target"])

    def rerank(self, out: dict, label: str, meaning: str, register: str, src: str) -> None:
        from .engines import verdict
        for c in out["candidates"]:
            c.update(verdict(c["lines"], label))
            c["reverse_nll"] = self.reverse_nll(label, c["lines"], meaning, register, src)
        out["candidates"].sort(key=lambda c: (-int(c["metre_ok"]), -int(c["prasa_relaxed"] and c["yati_relaxed"]),
                                              c["reverse_nll"], -c["logw"]))
        out["best"] = out["candidates"][0]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", type=Path, required=True, help="run directory, snapshot or model file")
    ap.add_argument("--metre", required=True, help='catalogue label, e.g. utpalamala or "seesamu+tetagiti"')
    ap.add_argument("--meaning", required=True)
    ap.add_argument("--register", default=CLASSICAL)
    for f in dataclasses.fields(DecodeConfig):
        ap.add_argument(f"--{f.name.replace('_', '-')}", type=type(f.default) if not isinstance(f.default, bool) else
                        (lambda s: s.lower() in ("1", "true", "yes")), default=f.default)
    args = ap.parse_args(argv)
    from tokenizer import load_default
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, _ = load_model(args.run, dev)
    cfg = DecodeConfig(**{f.name: getattr(args, f.name) for f in dataclasses.fields(DecodeConfig)})
    dec = Decoder(model, load_default(), dev, cfg)
    out = dec.generate(args.metre, args.meaning, args.register)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
