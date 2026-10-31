"""Turning (word, split) pairs into per-character labels for a BiLSTM tagger, and back.

The task follows Hellwig & Nehrdich (2018, EMNLP), who segment Sanskrit by labelling each
input character with the string it turns into in the segmented output. A sandhi split
can restore sounds as well as insert a boundary, so a label is a small rewrite:

    word   మీరెవరు            target  మీరు+ఎవరు
    labels మ:= ీ:= ర:= ె:"ు+ఎ" వ:= ర:= ు:=

Labels are stored relative to the input character: "=" stands for the character itself, so
"=+అ" means "keep the character, then a boundary, then అ". That keeps the label set small.
"""
import difflib
import re

TELUGU = re.compile(r"[ఀ-౿]+")
PAREN = re.compile(r"\([^)]*\)")
# A Telugu word (or split part) must start with an independent vowel or a consonant.
WORD_START = re.compile(r"^[అ-ఔక-హౘ-ౚౠ-ౡ]")
SEP = "+"
COPY = "="


def clean_word(raw):
    return "".join(TELUGU.findall(raw or ""))


def clean_split(raw):
    """'భానుడు + పోలె (commentary)' -> ['భానుడు', 'పోలె']; None/'' -> []"""
    if not raw:
        return []
    parts = ["".join(TELUGU.findall(p)) for p in PAREN.sub("", raw).split(SEP)]
    return [p for p in parts if p]


def char_labels(word, target):
    """Per-character output strings so that ''.join(outputs) == target."""
    out = [""] * len(word)
    prefix = ""
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, word, target, autojunk=False).get_opcodes():
        n, m = i2 - i1, j2 - j1
        if tag == "equal":
            for k in range(n):
                out[i1 + k] = target[j1 + k]
        elif tag == "insert":  # attach to the previous character (or the first one)
            if i1 == 0:
                prefix += target[j1:j2]
            else:
                out[i1 - 1] += target[j1:j2]
        elif tag == "replace":  # pair characters left to right; the last one takes the rest
            for k in range(n):
                if k < n - 1:
                    out[i1 + k] = target[j1 + k] if k < m else ""
                else:
                    out[i1 + k] = target[j1 + k:j2] if k < m else ""
        # "delete": characters map to ""
    if prefix:
        out[0] = prefix + out[0]
    return out


def encode(word, target):
    """Relative labels: '=' marks the input character itself."""
    labels = []
    for ch, o in zip(word, char_labels(word, target)):
        if o.startswith(ch):
            labels.append(COPY + o[1:])
        elif o.endswith(ch):
            labels.append(o[:-1] + COPY)
        else:
            labels.append(o if o else "<DEL>")
    return labels


def decode(word, labels):
    """Apply predicted labels; return the split string, or the word itself if no split."""
    pieces = []
    for ch, lab in zip(word, labels):
        if lab == "<DEL>":
            continue
        pieces.append(lab.replace(COPY, ch, 1) if COPY in lab else lab)
    out = "".join(pieces)
    parts = [p for p in out.split(SEP) if p]
    if len(parts) < 2:
        return word
    return SEP.join(parts)


def boundary_positions(labels):
    """Input-character indices whose label introduces a split boundary."""
    return {i for i, lab in enumerate(labels) if SEP in lab}
