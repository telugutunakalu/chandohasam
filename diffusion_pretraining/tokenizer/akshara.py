"""Telugu akshara (orthographic syllable) segmentation — dependency-free, regex-based.

Codepoint-order grammar (NOT rendering order):
    akshara := IV NUKTA? SIGN*                                    # independent vowel
             | C NUKTA? (VIRAMA C NUKTA?)* (MATRA LEN? | VIRAMA)? SIGN*
The vowel sign attaches to the LAST consonant of a conjunct, so a conjunct
C1 ್ C2 ್ C3 + matra is ONE akshara.  Greedy (VIRAMA C)* then an optional
trailing VIRAMA handles pollu / dead final consonants.
"""
import re, unicodedata

IV     = r"\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C14\u0C60\u0C61"   # independent vowels
C      = r"\u0C15-\u0C28\u0C2A-\u0C39\u0C58-\u0C5A\u0C5D"          # consonants (incl. ఴ ౘ ౙ ౚ ౝ)
MATRA  = r"\u0C3E-\u0C44\u0C46-\u0C48\u0C4A-\u0C4C\u0C62\u0C63"    # dependent vowel signs
LEN    = r"\u0C55\u0C56"                                            # length marks
VIRAMA = r"\u0C4D"
NUKTA  = r"\u0C3C"
SIGN   = r"\u0C00-\u0C04"                                           # candrabindu/anusvara/visarga

AKSHARA_RE = (
    f"[{IV}][{NUKTA}]?[{SIGN}]*"
    f"|[{C}][{NUKTA}]?(?:[{VIRAMA}][{C}][{NUKTA}]?)*"
    f"(?:[{MATRA}][{LEN}]?|[{VIRAMA}])?[{SIGN}]*"
    f"|\u0C3D"                       # avagraha, standalone
    f"|[\u0C66-\u0C6F]+"             # Telugu digits
    f"|[^\u0C00-\u0C7F]+"            # non-Telugu run (Latin, punct, spaces) -> passthrough
    f"|[\u0C00-\u0C7F]"              # orphan combining mark / stray sign -> never drop it
)
_AK = re.compile(AKSHARA_RE)

_ZW = re.compile("[\u200c\u200d\ufeff]")

def normalize(s: str) -> str:
    """NFC + strip zero-width joiners. Do this BEFORE segmenting, and before
    every corpus pass, or your akshara counts will not be reproducible."""
    return unicodedata.normalize("NFC", _ZW.sub("", s))

def aksharas(s: str, keep_nontelugu=True, merge_pollu=True):
    """Segment a normalized string into aksharas. Lossless: ''.join(out) == s.

    merge_pollu: a bare pollu (వాక్ -> వా|క్) carries no vowel, so it is NOT a
    syllable nucleus. For chandassu the coda must fold into the preceding akshara
    (వాక్ = 1 guru akshara, not 2). Set False only if you want pure orthographic
    grapheme clusters."""
    out = _AK.findall(s)
    if merge_pollu:
        m = []
        for a in out:
            if (m and a.endswith("\u0C4D") and a[0] in _CSET
                    and m[-1] and "\u0C00" <= m[-1][0] <= "\u0C7F"):
                m[-1] += a
            else:
                m.append(a)
        out = m
    if not keep_nontelugu:
        out = [a for a in out if "\u0C00" <= a[0] <= "\u0C7F"]
    return out

# ---------------- prosody (guru / laghu) ----------------
LONG_MATRA = set("\u0C3E\u0C40\u0C42\u0C44\u0C47\u0C48\u0C4B\u0C4C")   # ా ీ ూ ౄ ే ై ో ౌ
LONG_IV    = set("\u0C06\u0C08\u0C0A\u0C0C\u0C0F\u0C10\u0C13\u0C14\u0C60\u0C61")
NASALS     = set("\u0C01\u0C02\u0C03\u0C00\u0C04")                      # ఁ ం ః
_CSET      = set(chr(c) for c in list(range(0x0C15, 0x0C29)) + list(range(0x0C2A, 0x0C3A))
                 + [0x0C58, 0x0C59, 0x0C5A, 0x0C5D])

def is_conjunct(ak: str) -> bool:
    """True if the akshara opens with a consonant cluster (samyuktakshara)."""
    return "\u0C4D" in ak and not ak.endswith("\u0C4D")  # virama, but not a bare pollu

def is_pollu(ak: str) -> bool:
    return ak.endswith("\u0C4D")

def weights(aks, padanta_guru=True):
    """G/L string for a line. NOTE: weight is CONTEXTUAL — an akshara is guru if the
    NEXT akshara is a conjunct or a pollu. This is why a static per-token G/L table
    is wrong for the token-final akshara. Exceptions (ra-vattu etc.) go in Niruktha."""
    tel = [a for a in aks if a and "\u0C00" <= a[0] <= "\u0C7F" and a[0] not in NASALS]
    out = []
    for i, a in enumerate(tel):
        g = (any(ch in LONG_MATRA for ch in a)
             or a[0] in LONG_IV
             or any(ch in NASALS for ch in a)
             or is_pollu(a))          # own coda closes the syllable -> guru regardless of vowel length
        if not g and i + 1 < len(tel):
            nxt = tel[i + 1]
            g = is_conjunct(nxt) or is_pollu(nxt)
        if not g and i + 1 == len(tel) and padanta_guru:
            g = True
        out.append("G" if g else "L")
    return "".join(out), tel

if __name__ == "__main__":
    gold = {
        "తెలుగు":        ["తె", "లు", "గు"],
        "అక్క":          ["అ", "క్క"],
        "శ్రీకృష్ణుడు":   ["శ్రీ", "కృ", "ష్ణు", "డు"],
        "విద్యార్థి":     ["వి", "ద్యా", "ర్థి"],
        "సంస్కృతం":      ["సం", "స్కృ", "తం"],
        "చంద్రుడు":      ["చం", "ద్రు", "డు"],
        "ఐశ్వర్యం":       ["ఐ", "శ్వ", "ర్యం"],
        "నమస్కారం":      ["న", "మ", "స్కా", "రం"],
        "క్ష్మ":          ["క్ష్మ"],
        "వాక్":          ["వాక్"],
        "పద్యం":         ["ప", "ద్యం"],
    }
    ok = 0
    for w, g in gold.items():
        got = aksharas(normalize(w))
        flag = "ok " if got == g else "FAIL"
        ok += got == g
        print(f"{flag} {w:<16} -> {got}" + ("" if got == g else f"   expected {g}"))
    print(f"\n{ok}/{len(gold)} pass")

    line = "శ్రీకృష్ణుడు వచ్చెను"
    aks = aksharas(normalize(line))
    w, tel = weights(aks)
    print("\nlossless:", "".join(aks) == normalize(line))
    print("aksharas:", tel)
    print("weights :", w)


# ---------------- decode-time mask ----------------
COMBINING = set(chr(c) for c in list(range(0x0C3E, 0x0C4E))
                + list(range(0x0C00, 0x0C05)) + [0x0C3C, 0x0C55, 0x0C56])

def emittable(text: str) -> bool:
    """False for any char-fallback shard (orphan matra / bare virama / stray anusvara).
    Mask these out of the logits at generation. Keep them for ENCODING — they are what
    makes the tokenizer lossless on unseen aksharas. Asymmetric by design."""
    t = text.replace("\u2581", " ").strip()
    return not t or t[0] not in COMBINING

def blocks_next(prev_ak: str, next_ak: str) -> bool:
    """Pollu-final akshara + independent-vowel-initial akshara = dangling virama = invalid
    Telugu. Mask this transition. (Pollu + consonant is FINE: the coda migrates to the next
    onset, akshara count and guru/laghu are both invariant — verified.)"""
    return is_pollu(prev_ak) and bool(next_ak) and "\u0C05" <= next_ak[0] <= "\u0C14"