"""One tokenisation of the poems for every stage, with the option of re-joining words that the
editions break across a line end.

A పాదము may end inside a word (classical metre does not respect word boundaries), and the editions
sometimes mark it with a hyphen (భూ- / షిత) and often not at all (గ్రిం / దంటఁగ). Tokenising line by
line turns such a word into two fragments. With join_lines=True, the last token of a line and the
first of the next are merged when
  - the line ends with a hyphen, or
  - the line-end token is not a word on its own and the merged form is a dictionary word
    (headword, variant, inflection, generated form) or an attested form,
so that a line end after a complete word is never merged.

Usage
    from corpus_lines import iter_poems, poem_tokens
    for d in iter_poems():                     # the two Padyarchana JSON files
        toks = poem_tokens(d, decisions, join_lines=True)   # decisions = load_decisions()
The decisions are deterministic given the lexicon, so every stage (dictionary pass, contexts, joins)
sees the same tokens.
"""
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
TEL = re.compile(r"[ఀ-౿]+")
HYPHEN = re.compile(r"[-–—]\s*$")


def iter_poems(paths=None):
    paths = paths or sorted(DATA.glob("padyarchana_poems_v3.part*.json"))
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip().rstrip(",")
                if line.startswith("{"):
                    yield json.loads(line)


def poem_lines(d):
    return [l.strip() for l in (d.get("lines") or (d.get("text") or "").split("\n")) if l.strip()]


def _good(lex, w):
    return lex.status(w) is not None or lex.attested(w)


DECISIONS = HERE.parent / "results" / "padyarchana" / "line_join_decisions.json"


def load_decisions(path=DECISIONS):
    """The set of (line-end token, next-line token) pairs that make_joined_counts.py decided to merge."""
    import json as _json
    if not Path(path).exists():
        return set()
    return {tuple(x) for x in _json.load(open(path, encoding="utf-8"))}


def join_candidates(lex, last, first, hyphen):
    """Is this boundary a candidate for merging? A hyphen decides at once; otherwise the line-end
    token must not be a word on its own (గ్రిం, కశ్య, నాలకిం, బాణుం). The candidate's fate is then decided
    by make_joined_counts.py: the merged form must be a dictionary / attested word or split into
    all-known parts (గ్రిందంటఁగ = క్రిందు+అంటఁగ)."""
    if hyphen:
        return "merge"
    return "candidate" if not _good(lex, last) else "keep"


def boundaries(d):
    """(last token of a line, first token of the next, hyphen at the line end) for every line pair."""
    lines = poem_lines(d)
    out, prev = [], None
    for ln in lines:
        toks = TEL.findall(ln)
        if not toks:
            continue
        if prev is not None:
            out.append((prev[0], toks[0], prev[1]))
        prev = (toks[-1], bool(HYPHEN.search(ln)))
    return out


# Spacing rules (v16, on by default; CORPUS_SPACE_RULES=0 restores the v15 tokenisation). The editions put
# spaces inside sandhi strings, mostly at syllable boundaries ("మ్రోయ నేఁ డఱిగి" for మ్రోయనేఁడఱిగి =
# మ్రోయన్ + నేఁడు + అఱిగి; "పరవశుం డై" for పరవశుండై; "సమ మై" for సమమై). Two rules undo it, applied only where
# the gap between the tokens is whitespace (punctuation is a real boundary):
#   1. after an arasunna: a token ending in ఁ is joined with the next token;
#   2. a single-akshara token is joined with the previous token, unless it is a free-standing monosyllable
#      (the pronouns, demonstratives, interjections and imperatives below).
SPACE_RULES = os.environ.get("CORPUS_SPACE_RULES", "1") != "0"
FREE_MONOSYLLABLES = {"నా", "నీ", "నే", "మా", "మీ", "తా", "దా", "ఆ", "ఈ", "ఏ", "ఓ", "ఔ", "యా", "యీ", "యే", "యో",
                      "శ్రీ", "రా", "పో", "లే", "హా", "ఛీ", "ఆఁ", "ఓం"}
_SIGNS = set("ాిీుూృౄెేైొోౌ") | {"\u0c62", "\u0c63"}
_MODS = set("ంఁః")
VIRAMA = "\u0c4d"


def aksharas(w):
    """Number of aksharas: a consonant cluster joined by virama with its vowel sign and modifiers is one."""
    n, prev = 0, ""
    for c in w:
        if c in _SIGNS or c in _MODS or c == VIRAMA:
            pass
        elif prev == VIRAMA:
            pass  # second consonant of a conjunct
        else:
            n += 1
        prev = c
    return n


def poem_token_spans(d, decisions=None, join_lines=False, record=None, space_record=None, rules=None):
    """Tokens of a poem in order, each as (token, (first line, start), (last line, end)) in poem_lines(d).
    With join_lines, a line-end token and the next line's first token are merged when the pair is in
    `decisions` (a set from load_decisions) or the line ends with a hyphen (`record` receives (last, first,
    joined)); then the spacing rules apply (`rules`, default SPACE_RULES; `space_record` receives
    (previous, token, joined, rule))."""
    lines = poem_lines(d)
    rules = SPACE_RULES if rules is None else rules
    per_line = [[(m.group(), i, m.start(), m.end()) for m in TEL.finditer(ln)] for i, ln in enumerate(lines)]
    if not join_lines:
        return [(t, (i, s), (i, e)) for toks in per_line for t, i, s, e in toks]
    decisions = decisions or set()
    flat = []  # [token, start, end, gap_before_is_space]
    carry = None
    for i, toks in enumerate(per_line):
        if not toks:
            continue
        toks = [[t, (li, s), (li, e), None] for t, li, s, e in toks]
        for k in range(1, len(toks)):
            toks[k][3] = lines[i][toks[k - 1][2][1]:toks[k][1][1]].strip() == ""
        if carry is not None:
            c_tok, hyphen = carry
            if hyphen or (c_tok[0], toks[0][0]) in decisions:
                merged = c_tok[0] + toks[0][0]
                if record is not None:
                    record.append((c_tok[0], toks[0][0], merged))
                toks[0] = [merged, c_tok[1], toks[0][2], c_tok[3]]
            else:
                flat.append(c_tok)
                li, le = c_tok[2]
                toks[0][3] = lines[li][le:].strip() == "" and lines[i][:toks[0][1][1]].strip() == ""
            carry = None
        if i + 1 < len(lines):
            carry = (toks[-1], bool(HYPHEN.search(lines[i])))
            flat.extend(toks[:-1])
        else:
            flat.extend(toks)
    if carry is not None:
        flat.append(carry[0])
    if not rules:
        return [(t, s, e) for t, s, e, _ in flat]
    out = []
    for t, s, e, gap in flat:
        if out and gap:
            prev = out[-1][0]
            why = "arasunna" if prev.endswith("ఁ") else "single" if aksharas(t) == 1 and t not in FREE_MONOSYLLABLES else None
            if why:
                if space_record is not None:
                    space_record.append((prev, t, prev + t, why))
                out[-1] = (prev + t, out[-1][1], e)
                continue
        out.append((t, s, e))
    return out


def poem_tokens(d, decisions=None, join_lines=False, record=None, space_record=None, rules=None):
    """The tokens of poem_token_spans, without the spans."""
    return [t for t, _, _ in poem_token_spans(d, decisions, join_lines, record, space_record, rules)]


def span_text(d, start, end, lines=None):
    """The poem text a token spans, and 30-character windows to its left and right (as the context model sees them)."""
    lines = lines or poem_lines(d)
    (li, s), (lj, e) = start, end
    left = lines[li][max(0, s - 30):s]
    right = lines[lj][e:e + 30]
    return left, right
