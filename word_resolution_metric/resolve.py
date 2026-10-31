#!/usr/bin/env python3
"""Minimal, self-contained word resolution for classical Telugu (Padyarchana / padarchana.db).

Given a word as it stands in a poem (and optionally its line), return the dictionary headword(s) it stands for.

Resolution order for one word:
  1. the precomputed table (data/resolved_words_v28.tsv.gz): every word type of the Padyarchana corpus with the
     pipeline's class, analysis and confidence — instant, and the best answer for any corpus word;
  2. the guaranteed table (rules/guaranteed.tsv): closed-class words and judge-confirmed answers;
  3. the lexicon (resolver/lexicon.py over db/padarchana_min.db): headwords, variants, inflections, particles, the
     sandhi rules (initial voicing, యడాగమ, drutam, syncope, Sanskrit stems, త్రిక …);
  4. the distilled ByT5 (models/byt5_distill_v2, optional, needs torch + transformers): an n-best analysis of a word
     the lexicon cannot read, accepted when every part is a dictionary word (the pipeline's "resolved-by-byt5");
  5. otherwise "unresolved".

    from resolve import WordResolver
    r = WordResolver()                      # loads the table lazily on first use; ByT5 only when needed
    r.resolve("లోకములోనఁ")                  # → {'word': …, 'class': 'inflected', 'analysis': 'లోకములోనఁ→లోకము', 'parts': [...], ...}
    r.resolve_line("వేమననగ యోగి వెలసె లోకములోనఁ")
    r.meanings("లోకము")                       # the dictionaries' definitions for a headword

    python resolve.py లోకములోనఁ వేమననగ            # CLI; --line "…" resolves a whole line; --json for JSON; --no-byt5 to skip the model
"""
import argparse
import gzip
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("LEXICON_FORMS_DB", str(ROOT / "db" / "paradigm_forms.db"))   # optional paradigm index (see README)
os.environ.setdefault("LEXICON_EXCLUDE_DICTS", "47,48,49,50")                         # the dictionaries kept out of the lexicon
os.environ.setdefault("LEXICON_SANDHI_PREFERENCE", "1")
sys.path.insert(0, str(ROOT / "resolver"))
from lexicon import Lexicon, normalize  # noqa: E402

SEP = "+"
STRONG = {"headword", "inflected", "split-all-known", "annotated-all-known", "resolved-by-byt5", "resolved-by-resolver", "split-parts-resolved"}
TEL = re.compile(r"[ఀ-౿]+")


class WordResolver:
    def __init__(self, root=ROOT, use_byt5=True, byt5_beams=4, device=None, glossary=True):
        self.root = Path(root)
        # glossary=True loads the Padyarchana editorial word glosses (padyarchana_forms) as attestation and gloss
        # evidence inside the lexicon, as the pipeline's attest and final stages do; the table itself is queried by .glossary()
        self.lex = Lexicon(db=str(self.root / "db" / "padarchana_min.db"), padyarchana=glossary)
        self.lex.headword_freq = self.lex.headword_freq or {}
        self._table = None
        self._rules = None
        self.use_byt5, self.byt5_beams, self.device = use_byt5, byt5_beams, device
        self._byt5 = None
        self._decisions = None

    # ---- data loaded on first use -----------------------------------------------------------------------------
    @property
    def table(self):
        if self._table is None:
            self._table = {}
            p = self.root / "data" / "resolved_words_v28.tsv.gz"
            if p.exists():
                with gzip.open(p, "rt", encoding="utf-8") as f:
                    header = f.readline().rstrip("\n").split("\t")
                    iw, ic, ia, iconf, isrc, icnt = (header.index(k) for k in ("word", "resolution", "analysis", "confidence", "source", "count"))
                    for line in f:
                        r = line.rstrip("\n").split("\t")
                        if len(r) > icnt:
                            self._table[r[iw]] = (r[ic], r[ia], float(r[iconf] or 0), r[isrc], int(r[icnt]))
        return self._table

    @property
    def rules(self):
        if self._rules is None:
            self._rules = {}
            p = self.root / "rules" / "guaranteed.tsv"
            if p.exists():
                with open(p, encoding="utf-8") as f:
                    header = f.readline().rstrip("\n").split("\t")
                    iw, ia, isrc, iconf = (header.index(k) for k in ("word", "analysis", "source", "confidence"))
                    for line in f:
                        r = line.rstrip("\n").split("\t")
                        if len(r) > iconf:
                            self._rules[r[iw]] = (r[ia], r[isrc], float(r[iconf] or 1))
        return self._rules

    @property
    def byt5(self):
        if self._byt5 is None and self.use_byt5:
            try:
                from byt5_splitter import ByT5Splitter
                self._byt5 = ByT5Splitter(checkpoint=self.root / "models" / "byt5_distill_v2", device=self.device,
                                          cache=self.root / "data" / "byt5_cache.json")
                import atexit
                atexit.register(lambda: (self._byt5.save(), getattr(self._byt5, "save_nbest", lambda: None)()))  # keep the generations
            except Exception as e:  # torch / transformers missing, or no model folder
                print(f"ByT5 unavailable ({e}); continuing without it", file=sys.stderr)
                self.use_byt5 = False
        return self._byt5

    # ---- analyses ----------------------------------------------------------------------------------------------
    def parts_of(self, analysis):
        """[{surface, headword, status}] for an analysis in the project's notation (a+b, a→h+b, [x]+y | z → h)."""
        out = []
        a = (analysis or "").split("=")[-1].replace("→ ", "→")
        for p in re.split(r"[+ |]", a):
            p = p.strip().strip("[]")
            if not p or re.search(r"[A-Za-z]", p):
                continue
            if "→" in p:
                surface, head = p.split("→")[0].strip(), p.split("→")[-1].strip()
                out.append({"surface": surface, "headword": head, "status": "given"})
            else:
                st, head, how = self.lex.resolve(p)
                out.append({"surface": p, "headword": head if st else None, "status": st or "unknown"})
        return out

    def _result(self, word, cls, analysis, confidence, source):
        parts = self.parts_of(analysis)
        return {"word": word, "class": cls, "resolved": cls in STRONG, "analysis": analysis, "parts": parts,
                "headwords": [p["headword"] for p in parts if p["headword"]], "confidence": round(float(confidence), 3), "source": source}

    def resolve(self, word, use_table=True):
        w = word.strip()
        if not w or not TEL.search(w):
            return self._result(w, "not-telugu", w, 0.0, "none")
        if use_table and w in self.table:
            cls, an, conf, src, cnt = self.table[w]
            return dict(self._result(w, cls, an, conf, f"table:{src}"), corpus_count=cnt)
        if w in self.rules:
            an, src, conf = self.rules[w]
            return self._result(w, "split-all-known" if SEP in an else ("headword" if an == w else "inflected"), an, conf, f"rule:{src}")
        st, head, how = self.lex.resolve(w)
        if st in ("headword", "variant", "redirect", "synonym"):
            return self._result(w, "headword", w if head == w else f"{w}→{head}", 1.0, f"lexicon:{how}")
        if st in ("inflected", "stem"):
            k = how or ""
            if k.startswith("particle:"):
                return self._result(w, "inflected", f"{head}+{k.split(':')[1].split('+')[0]}", 0.9, f"lexicon:{k}")
            if k.startswith("trika:"):
                return self._result(w, "split-all-known", f"{k.split(':')[1]}+{k.split(':')[2]}→{head}", 0.9, f"lexicon:{k}")
            return self._result(w, "inflected", f"{w}→{head}", 0.9 if "generated" in k else 0.6, f"lexicon:{k}")
        if self.use_byt5 and self.byt5 is not None:
            for rank, an in enumerate(self._byt5_nbest(w)):
                parts = self.parts_of(an)
                if parts and all(p["headword"] for p in parts):
                    return self._result(w, "resolved-by-byt5", an, 0.79 if rank == 0 else 0.70, f"byt5:beam{rank + 1}")
        return self._result(w, "unresolved", w, 0.0, "none")

    def _byt5_nbest(self, word):
        try:
            res = self.byt5.headwords_nbest([word], n=self.byt5_beams)
            cands = res.get(word, res) if isinstance(res, dict) else res[0]
            return [c for c in (cands if isinstance(cands, list) else [cands]) if isinstance(c, str)]
        except Exception as e:
            print(f"ByT5 failed on {word}: {e}", file=sys.stderr)
            return []

    # ---- lines and poems ---------------------------------------------------------------------------------------
    def tokens(self, lines):
        """The pipeline's tokens of one or more poem lines (line-end joins by the recorded decisions, v16 spacing rules)."""
        from corpus_lines import load_decisions, poem_tokens
        if self._decisions is None:
            self._decisions = load_decisions(self.root / "data" / "line_join_decisions.json")
        return poem_tokens({"lines": lines}, self._decisions, join_lines=True)

    def resolve_line(self, line):
        return [self.resolve(t) for t in self.tokens([line])]

    def resolve_poem(self, lines):
        return [self.resolve(t) for t in self.tokens(list(lines))]

    # ---- the poems' word-by-word glossary -----------------------------------------------------------------------
    def glossary(self, word, layer=None, limit=20):
        """Entries of the Padyarchana glossary (padyarchana_forms) for a word as it stands in the poems:
        [{form, layer, gloss, gloss_en, split, attestations (poems with this form+gloss), poem_id (one example),
          status (the lexicon's reading of the form), headword}]. layer: 'editorial' (human), 'generated' (machine) or None."""
        con = self.lex.con
        q = "select form, layer, gloss, gloss_en, split, attestations, poem_id, status, headword from padyarchana_forms where form_norm = ?"
        args = [normalize(word)]
        if layer:
            q += " and layer = ?"; args.append(layer)
        q += " order by case layer when 'editorial' then 0 else 1 end, attestations desc limit ?"; args.append(limit)
        try:
            rows = con.execute(q, args).fetchall()
        except Exception:
            return []
        keys = ("form", "layer", "gloss", "gloss_en", "split", "attestations", "poem_id", "status", "headword")
        return [dict(zip(keys, r)) for r in rows]

    # ---- the dictionaries --------------------------------------------------------------------------------------
    def meanings(self, headword, limit=12):
        """Definitions of a headword from padarchana_min.db: [(dictionary, grammar, meaning text)]."""
        con = self.lex.con
        rows = con.execute(
            "select dc.name, coalesce(g.grammar_raw, ''), m.text from entries e join definitions d on d.entry_id = e.id "
            "join dictionaries dc on dc.dict_id = d.dict_id left join grammar g on g.g_id = d.g_id "
            "join meanings m on m.def_id = d.def_id where e.word in (?, ?) order by d.dict_id, d.ord, m.ord limit ?",
            (headword, normalize(headword), limit)).fetchall()
        return [{"dictionary": n, "grammar": g, "meaning": t} for n, g, t in rows]


def main():
    ap = argparse.ArgumentParser(description="resolve classical Telugu words to padarchana headwords")
    ap.add_argument("words", nargs="*")
    ap.add_argument("--line", help="resolve every word of this poem line")
    ap.add_argument("--meanings", action="store_true", help="also print the dictionaries' definitions of each headword")
    ap.add_argument("--glossary", action="store_true", help="also print the poems' glossary entries for each word (editorial first)")
    ap.add_argument("--no-table", action="store_true", help="ignore the precomputed corpus table (exercise the live resolver)")
    ap.add_argument("--no-byt5", action="store_true", help="do not load the ByT5 model")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = WordResolver(use_byt5=not a.no_byt5)
    results = r.resolve_line(a.line) if a.line else [r.resolve(w, use_table=not a.no_table) for w in a.words]
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        return
    for res in results:
        heads = ", ".join(res["headwords"]) or "—"
        print(f"{res['word']:22} {res['class']:20} {res['analysis']:36} → {heads}   [{res['source']}, {res['confidence']}]")
        if a.glossary:
            for g in r.glossary(res["word"], limit=4):
                print(f"      glossary [{g['layer']}, {g['attestations']} poems]: {g['form']}" + (f" = {g['split']}" if g['split'] else "") + f" : {g['gloss'][:90]}")
        if a.meanings:
            for h in res["headwords"][:3]:
                for m in r.meanings(h, limit=3):
                    print(f"      {h} · {m['dictionary'][:28]}: {m['meaning'][:110]}")


if __name__ == "__main__":
    main()
