import re
import unicodedata
from collections import Counter


class AlankaramChecker:
    """
    Akshara segmentation + vRttyanuprAsa detection for Telugu, Devanagari
    and Harvard-Kyoto (HK) input.

    Script text is parsed straight from Unicode into Harvard-Kyoto
    labels (plain a-z/A-Z, no diacritics). Telugu short/long vowels use
    e/E and o/O; ళ = L, ఱ = R (consonant), arasunna = M.
    Telugu and Devanagari share the same ISCII-derived
    block layout, so one offset table serves both.

    vRttyanuprAsa detection (consonant_skeleton / check_vrutyanuprasa) is
    kept on its own vowel-free path, separate from the full akshara
    syllabification (parse_aksharas / get_aksharas) that other uses —
    e.g. laghu/guru marking — need vowel length for.
    """

    # ---- Unicode tables (offset from block start: Telugu U+0C00, Devanagari U+0900)
    # All labels are Harvard-Kyoto (plain a-z / A-Z, no diacritics).
    CONSONANTS = {
        0x15: 'k', 0x16: 'kh', 0x17: 'g', 0x18: 'gh', 0x19: 'G',
        0x1A: 'c', 0x1B: 'ch', 0x1C: 'j', 0x1D: 'jh', 0x1E: 'J',
        0x1F: 'T', 0x20: 'Th', 0x21: 'D', 0x22: 'Dh', 0x23: 'N',
        0x24: 't', 0x25: 'th', 0x26: 'd', 0x27: 'dh', 0x28: 'n', 0x29: 'n',
        0x2A: 'p', 0x2B: 'ph', 0x2C: 'b', 0x2D: 'bh', 0x2E: 'm',
        0x2F: 'y', 0x30: 'r', 0x31: 'R', 0x32: 'l', 0x33: 'L', 0x34: 'L',
        0x35: 'v', 0x36: 'z', 0x37: 'S', 0x38: 's', 0x39: 'h',
    }
    TELUGU_EXTRA_CONSONANTS = {0x58: 'ts', 0x59: 'dz', 0x5A: 'R'}  # ౘ ౙ ౚ

    # Vowels common to both scripts
    INDEPENDENT_VOWELS = {
        0x05: 'a', 0x06: 'A', 0x07: 'i', 0x08: 'I', 0x09: 'u', 0x0A: 'U',
        0x0B: 'R', 0x0C: 'lR', 0x10: 'ai', 0x14: 'au', 0x60: 'RR', 0x61: 'lRR',
    }
    VOWEL_SIGNS = {
        0x3E: 'A', 0x3F: 'i', 0x40: 'I', 0x41: 'u', 0x42: 'U',
        0x43: 'R', 0x44: 'RR', 0x48: 'ai', 0x4C: 'au', 0x62: 'lR', 0x63: 'lRR',
    }
    # e/o differ by script: Telugu has short e/o vs long E/O;
    # in Sanskrit (Devanagari) e/o are inherently long, so plain HK e/o.
    SCRIPT_E_O = {
        'telugu': {0x0E: 'e', 0x0F: 'E', 0x12: 'o', 0x13: 'O',      # independent
                   0x46: 'e', 0x47: 'E', 0x4A: 'o', 0x4B: 'O'},     # mAtras
        'devanagari': {0x0E: 'e', 0x0F: 'e', 0x12: 'o', 0x13: 'o',
                       0x46: 'e', 0x47: 'e', 0x4A: 'o', 0x4B: 'o'},
    }
    INDEPENDENT_E_O = {0x0E, 0x0F, 0x12, 0x13}
    SIGN_E_O = {0x46, 0x47, 0x4A, 0x4B}

    MODIFIERS = {0x01: 'M', 0x02: 'M', 0x03: 'H'}   # arasunna/candrabindu -> M, anusvAra, visarga
    VIRAMA = 0x4D
    NUKTA = 0x3C
    IGNORED = {0x3D, 0x55, 0x56}                      # avagraha, Telugu length marks
    ZERO_WIDTH = {'\u200c', '\u200d'}

    # ---- Harvard-Kyoto input tables
    HK_CONSONANTS = {
        'kh': 'kh', 'gh': 'gh', 'ch': 'ch', 'jh': 'jh', 'Th': 'Th', 'Dh': 'Dh',
        'th': 'th', 'dh': 'dh', 'ph': 'ph', 'bh': 'bh',
        'k': 'k', 'g': 'g', 'G': 'G', 'c': 'c', 'j': 'j', 'J': 'J',
        'T': 'T', 'D': 'D', 'N': 'N', 't': 't', 'd': 'd', 'n': 'n',
        'p': 'p', 'b': 'b', 'm': 'm', 'y': 'y', 'r': 'r', 'l': 'l', 'L': 'L',
        'v': 'v', 'z': 'z', 'S': 'S', 's': 's', 'h': 'h',
    }
    HK_VOWELS = {
        'ai': 'ai', 'au': 'au', 'RR': 'RR',
        'a': 'a', 'A': 'A', 'i': 'i', 'I': 'I', 'u': 'u', 'U': 'U',
        'R': 'R', 'e': 'e', 'E': 'E', 'o': 'o', 'O': 'O',
    }
    HK_VOWEL_LETTERS = set('aAiIuUeEoO')
    HK_MODIFIERS = {'M': 'M', 'H': 'H'}

    # ---- Phonetic equivalence classes for the "Equivalent" check
    DEFAULT_EQUIVALENCES = {
        'k': 'kh', 'g': 'gh', 'c': 'ch', 'j': 'jh', 'T': 'Th', 'D': 'Dh', 't': 'th', 'd': 'dh', 'p': 'ph', 'b': 'bh',  # aspirated vs unaspirated
        'm': 'M', 'h': 'H',                     # nasals / aspiration
        'z': 's', 'S': 's', 's': 's',   # sibilants (z = sh, S = retroflex sh)
        'N': 'n', 'n': 'n',             # retroflex / dental nasal
        'L': 'l', 'l': 'l',             # ళ / ల
        'R': 'r', 'r': 'r',             # ఱ / ర  (consonant R, never the vowel)
    }

    # ------------------------------------------------------------------ utils
    @staticmethod
    def _locate(ch):
        cp = ord(ch)
        if 0x0C00 <= cp <= 0x0C7F:
            return 'telugu', cp - 0x0C00
        if 0x0900 <= cp <= 0x097F:
            return 'devanagari', cp - 0x0900
        return None, None

    def detect_script(self, text):
        for ch in text:
            script, _ = self._locate(ch)
            if script:
                return script
        return 'hk'

    def _consonant(self, script, off):
        if off in self.CONSONANTS:
            return self.CONSONANTS[off]
        if script == 'telugu':
            return self.TELUGU_EXTRA_CONSONANTS.get(off)
        return None

    # --------------------------------------------------- phoneme streams
    # Both front-ends yield ('C', cons) / ('V', vowel) / ('M', modifier) / ('B', None).
    def _script_stream(self, text):
        chars = unicodedata.normalize('NFC', text)   # also splits क़ → क + ़
        n, i = len(chars), 0
        while i < n:
            ch = chars[i]
            script, off = self._locate(ch)
            if script is None:
                i += 1
                if ch not in self.ZERO_WIDTH:
                    yield ('B', None)
                continue

            cons = self._consonant(script, off)
            if cons:
                yield ('C', cons)
                i += 1
                while i < n and (chars[i] in self.ZERO_WIDTH or self._locate(chars[i]) == (script, self.NUKTA)):
                    i += 1
                nxt_script, nxt_off = self._locate(chars[i]) if i < n else (None, None)
                if nxt_script == script and nxt_off in self.VOWEL_SIGNS:
                    yield ('V', self.VOWEL_SIGNS[nxt_off])
                    i += 1
                elif nxt_script == script and nxt_off in self.SIGN_E_O:
                    yield ('V', self.SCRIPT_E_O[script][nxt_off])
                    i += 1
                elif nxt_script == script and nxt_off == self.VIRAMA:
                    i += 1                      # pollu / conjunct: no vowel
                else:
                    yield ('V', 'a')            # inherent vowel
            elif off in self.INDEPENDENT_VOWELS:
                yield ('V', self.INDEPENDENT_VOWELS[off])
                i += 1
            elif off in self.INDEPENDENT_E_O:
                yield ('V', self.SCRIPT_E_O[script][off])
                i += 1
            elif off in self.MODIFIERS:
                yield ('M', self.MODIFIERS[off])
                i += 1
            elif off in self.IGNORED or off == self.NUKTA:
                i += 1
            else:                               # danda, digits, etc.
                yield ('B', None)
                i += 1

    def _hk_stream(self, text):
        n, i = len(text), 0
        while i < n:
            # 'R' followed by a vowel is the consonant ఱ, otherwise vocalic R
            if text[i] == 'R' and text[i + 1:i + 2] in self.HK_VOWEL_LETTERS:
                yield ('C', 'R')
                i += 1
                continue
            for table, kind in ((self.HK_VOWELS, 'V'), (self.HK_CONSONANTS, 'C'), (self.HK_MODIFIERS, 'M')):
                two = text[i:i + 2]
                if len(two) == 2 and two in table:
                    yield (kind, table[two])
                    i += 2
                    break
                if text[i] in table:
                    yield (kind, table[text[i]])
                    i += 1
                    break
            else:
                yield ('B', None)
                i += 1

    # --------------------------------------------------- vowel-free skeleton
    def consonant_skeleton(self, text):
        """
        Return the consonant skeleton of `text` as a list of onset-groups
        (each a tuple of one or more HK consonant labels joined into a
        single saṃyuktākṣara). This never consults a vowel table — script
        input only ever asks "is this a consonant?" (CONSONANTS /
        TELUGU_EXTRA_CONSONANTS) or "is this a virama?"; anything else
        (matra, independent vowel, arasunna/anusvara/visarga, punctuation,
        whitespace) just closes the current group without being inspected.

        The one unavoidable exception is HK 'R', which is genuinely
        ambiguous between the consonant ఱ and vocalic ṛ; disambiguating it
        means checking whether the next letter is *a* vowel, though never
        which one.
        """
        return (self._consonant_skeleton_hk(text) if self.detect_script(text) == 'hk'
                else self._consonant_skeleton_script(text))

    def _consonant_skeleton_script(self, text):
        chars = unicodedata.normalize('NFC', text)
        n, i = len(chars), 0
        groups, pending = [], []
        while i < n:
            script, off = self._locate(chars[i])
            cons = self._consonant(script, off) if script else None
            if cons is None:
                if pending:
                    groups.append(tuple(pending))
                    pending.clear()
                i += 1
                continue
            pending.append(cons)
            i += 1
            while i < n and (chars[i] in self.ZERO_WIDTH or self._locate(chars[i]) == (script, self.NUKTA)):
                i += 1
            if i < n and self._locate(chars[i]) == (script, self.VIRAMA):
                i += 1
                continue          # virama: next consonant joins this group
            groups.append(tuple(pending))
            pending.clear()
        if pending:
            groups.append(tuple(pending))
        return groups

    def _consonant_skeleton_hk(self, text):
        n, i = len(text), 0
        groups, pending = [], []
        while i < n:
            if text[i] == 'R' and text[i + 1:i + 2] in self.HK_VOWEL_LETTERS:
                pending.append('R')                    # ఱ, not vocalic R
                i += 1
                continue
            two = text[i:i + 2]
            if two in self.HK_CONSONANTS:
                pending.append(self.HK_CONSONANTS[two])
                i += 2
                continue
            if text[i] in self.HK_CONSONANTS:
                pending.append(self.HK_CONSONANTS[text[i]])
                i += 1
                continue
            if pending:
                groups.append(tuple(pending))
                pending.clear()
            i += 1
        if pending:
            groups.append(tuple(pending))
        return groups

    # ------------------------------------------------------ syllabification
    def parse_aksharas(self, text):
        """Return a list of dicts: {'onset': tuple, 'vowel': str, 'coda': str}."""
        stream = self._hk_stream(text) if self.detect_script(text) == 'hk' else self._script_stream(text)
        aksharas, pending = [], []

        def flush_pollu():
            if pending:
                aksharas.append({'onset': tuple(pending), 'vowel': '', 'coda': ''})
                pending.clear()

        for kind, val in stream:
            if kind == 'C':
                pending.append(val)
            elif kind == 'V':
                aksharas.append({'onset': tuple(pending), 'vowel': val, 'coda': ''})
                pending.clear()
            elif kind == 'M':
                flush_pollu()
                if aksharas:
                    aksharas[-1]['coda'] += val
            else:  # boundary
                flush_pollu()
        flush_pollu()
        return aksharas

    def get_aksharas(self, text):
        return [''.join(a['onset']) + a['vowel'] + a['coda'] for a in self.parse_aksharas(text)]

    # --------------------------------------------------------- alaṅkāra
    def check_vrutyanuprasa(self, lines, min_repeats=3, equivalences=None):
        eq = self.DEFAULT_EQUIVALENCES if equivalences is None else equivalences
        results = []

        for line_no, line in enumerate(lines, 1):
            groups = self.consonant_skeleton(line)          # vowel-free
            consonants = [c for g in groups for c in g]
            clusters = [''.join(g) for g in groups if len(g) > 1]
            position = f"Line {line_no}"

            # 1. Single consonant repetition
            for cons, count in Counter(consonants).most_common():
                if count >= min_repeats:
                    results.append({
                        "alankaram": "Vrutyanuprasa Alankaram (Direct)",
                        "trigger": f"Consonant '{cons}' repeated {count} times",
                        "position": position,
                        "repeat_count": count,
                    })

            # 2. Consonant-cluster (saṃyuktākṣara) repetition
            for cluster, count in Counter(clusters).most_common():
                if count >= min_repeats:
                    results.append({
                        "alankaram": "Vrutyanuprasa Alankaram (Cluster)",
                        "trigger": f"Cluster '{cluster}' repeated {count} times",
                        "position": position,
                        "repeat_count": count,
                    })

            # 3. Equivalent-sound repetition: only when ≥2 distinct members
            #    contribute, otherwise it is just a duplicate of the Direct hit.
            groups = {}
            for cons in consonants:
                if cons in eq:
                    groups.setdefault(eq[cons], Counter())[cons] += 1
            for cls, members in groups.items():
                total = sum(members.values())
                if len(members) > 1 and total >= min_repeats:
                    detail = ", ".join(f"{m}:{k}" for m, k in members.most_common())
                    results.append({
                        "alankaram": "Vrutyanuprasa Alankaram (Equivalent)",
                        "trigger": f"Equivalent sound '{cls}' ({detail}) repeated {total} times",
                        "position": position,
                        "repeat_count": total,
                    })

        return results or None

    # --------------------------------------------------------- alaṅkāra
    _WORD_BOUNDARY_RE = re.compile(r'[\s,;:।॥!?.]+')
    _VOWEL_LENGTH_TABLE = str.maketrans({'A': 'a', 'I': 'i', 'U': 'u', 'E': 'e', 'O': 'o'})

    def _split_words(self, text):
        return [w for w in self._WORD_BOUNDARY_RE.split(text.strip()) if w]

    def _normalize_vowel_length(self, s):
        """Collapse long vowels to their short counterpart (a/A, i/I, u/U,
        e/E, o/O, vocalic R/RR) — antyAnuprAsa is judged by vowel quality,
        not length, so 'la' and 'lA' should count as the same ending.
        ai/au have no short counterpart and are left as-is."""
        return s.replace('RR', 'R').translate(self._VOWEL_LENGTH_TABLE)

    def _ending(self, text, suffix_len, equivalences=None):
        """Last `suffix_len` aksharas of `text`, normalized for
        antyAnuprAsa comparison: vowel LENGTH is ignored (see
        _normalize_vowel_length) and onset consonants are folded through
        `equivalences` (default DEFAULT_EQUIVALENCES — the same
        sibilant/retroflex classes as vRttyanuprAsa's Equivalent check,
        e.g. స/శ both count as the same ending-consonant). Vowel quality
        and any consonant distinction outside those classes still counts.
        None if text is too short."""
        eq = self.DEFAULT_EQUIVALENCES if equivalences is None else equivalences
        aksharas = self.parse_aksharas(text)
        if len(aksharas) < suffix_len:
            return None
        parts = []
        for ak in aksharas[-suffix_len:]:
            onset = ''.join(eq.get(c, c) for c in ak['onset'])
            vowel = self._normalize_vowel_length(ak['vowel'])
            parts.append(onset + vowel + ak['coda'])
        return ''.join(parts)

    def check_antyanuprasa(self, lines, suffix_len=1, min_repeats=2, equivalences=None):
        """
        Detect antyAnuprAsa: the same akshara(s) — vowel quality, not
        length (see _normalize_vowel_length) — recurring at the end of
        successive words within a pAda, or at the end of successive pAdas
        across the WHOLE passage in `lines`.

        Each item in `lines` is one pAda by default; an item may itself
        hold several '\\n'-separated pAdas (a whole stanza as one string).
        PAda-final matching spans every pAda in the input regardless of
        which list item or '\\n'-group it came from — a rhyme between the
        last two lines of a padyam should be caught whether they arrived
        as one string or as two separate list entries.
        """
        results = []

        # Flatten every pAda in the whole input, remembering where it came from.
        all_padas = []   # (position_label, pada_text)
        for line_no, block in enumerate(lines, 1):
            sub_padas = [p.strip() for p in block.split('\n') if p.strip()]
            multi = len(sub_padas) > 1
            for pada_no, pada in enumerate(sub_padas, 1):
                label = f"Line {line_no}, Pada {pada_no}" if multi else f"Line {line_no}"
                all_padas.append((label, pada))

        # 1. PAda-final: same ending shared across pAdas anywhere in the input
        pada_groups = {}
        for label, pada in all_padas:
            ending = self._ending(pada, suffix_len, equivalences)
            if ending:
                pada_groups.setdefault(ending, []).append((label, pada))
        for ending, matched in pada_groups.items():
            texts = [p for _, p in matched]
            if len(matched) >= min_repeats and len(set(texts)) > 1:
                results.append({
                    "alankaram": "Antyanuprasa Alankaram (Pada-final)",
                    "trigger": f"Ending '{ending}' shared by {len(matched)} pAdas: {texts}",
                    "position": "; ".join(l for l, _ in matched),
                    "repeat_count": len(matched),
                })

        # 2. Word-final: same ending shared across distinct words, within
        #    each pAda separately.
        for label, pada in all_padas:
            word_groups = {}
            for w in self._split_words(pada):
                ending = self._ending(w, suffix_len, equivalences)
                if ending:
                    word_groups.setdefault(ending, []).append(w)
            for ending, matched in word_groups.items():
                if len(matched) >= min_repeats and len(set(matched)) > 1:
                    results.append({
                        "alankaram": "Antyanuprasa Alankaram (Word-final)",
                        "trigger": f"Ending '{ending}' shared by {len(matched)} words: {matched}",
                        "position": label,
                        "repeat_count": len(matched),
                    })

        return results or None

    # --------------------------------------------------------- alaṅkāra
    def check_chekanuprasa(self, lines, min_pair_len=2, equivalences=None):
        """
        Detect chekAnuprAsa: a consonant sequence of length >= `min_pair_len`
        recurring with NO gap between the two occurrences. This is judged
        on the pAda's whole consonant stream, words run together — a
        written space is not a phonetic gap, and Sanskrit/Telugu compounds
        (samAsa) routinely put the repeat entirely inside one written word
        (e.g. kandarpa-DARPA-bhaMga, where "darpa" is both the tail of
        "kandarpa" and the whole of the next morpheme). Only a repeat that
        turns out to be two entire, identical words is excluded, as plain
        reduplication/refrain rather than chekAnuprAsa (the classical
        requirement is a meaning shift between occurrences, which an
        identical whole word repeated verbatim doesn't have; this is
        otherwise unverifiable here without real morphological analysis,
        so anything short of that exact case is left for you to judge).

        Vowel-free, like vRttyanuprAsa's consonant_skeleton (it is the
        CONSONANT sequence that must recur, not the syllable, unlike
        antyAnuprAsa). `equivalences` optionally folds consonants through
        a class map (e.g. DEFAULT_EQUIVALENCES) before comparing; off by
        default since the classical examples rely on exact identity.
        The longest qualifying match at each position is reported, since
        the classical wording allows "two or more" consonants.
        """
        results = []
        for line_no, block in enumerate(lines, 1):
            padas = [p.strip() for p in block.split('\n') if p.strip()]
            multi = len(padas) > 1
            for pada_no, pada in enumerate(padas, 1):
                label = f"Line {line_no}, Pada {pada_no}" if multi else f"Line {line_no}"
                words = self._split_words(pada)
                if not words:
                    continue

                # One flat consonant stream for the whole pAda; remember
                # each word's [start, end) span within it.
                stream, spans = [], []
                for w in words:
                    start = len(stream)
                    for g in self.consonant_skeleton(w):
                        stream.extend(g)
                    spans.append((start, len(stream), w))
                if equivalences:
                    stream = [equivalences.get(c, c) for c in stream]

                n = len(stream)
                for i in range(n):
                    best_k = 0
                    for k in range(min_pair_len, (n - i) // 2 + 1):
                        if stream[i:i + k] == stream[i + k:i + 2 * k]:
                            best_k = k        # keep extending to the longest
                    if not best_k:
                        continue
                    j, end = i + best_k, i + 2 * best_k
                    w1 = next((w for s, e, w in spans if s == i and e == j), None)
                    w2 = next((w for s, e, w in spans if s == j and e == end), None)
                    if w1 is not None and w2 is not None and w1 == w2:
                        continue              # two whole, identical words: plain repeat
                    results.append({
                        "alankaram": "Chekanuprasa Alankaram",
                        "trigger": f"Consonant sequence '{'+'.join(stream[i:j])}' "
                                   f"({best_k}-long) repeats with no gap",
                        "position": label,
                        "repeat_count": best_k,
                    })
        return results or None
    
      # --------------------------------------------------------- alaṅkāra
    def _flatten_padas(self, lines):
        """Every pAda in the input, in reading order, as (label, text).
        Each item in `lines` is one pAda; an item may hold several
        '\\n'-separated pAdas."""
        out = []
        for line_no, block in enumerate(lines, 1):
            subs = [p.strip() for p in block.split('\n') if p.strip()]
            for pada_no, pada in enumerate(subs, 1):
                label = f"Line {line_no}, Pada {pada_no}" if len(subs) > 1 else f"Line {line_no}"
                out.append((label, pada))
        return out
 
    def check_muktapadagrastam(self, lines, min_len=2):
        """
        Detect muktapadagrastamu: the word (or subword) a pAda ends with
        is taken up again at the start of the very next pAda.
 
        Compared as aksharas, vowels included and vowel length kept — it
        is the same word being reused, so it must match as written. The
        longest match across the line-end / line-start is reported, and it
        may run over several words or start mid-word (subword).
        A match shorter than `min_len` aksharas is accepted only when it
        is a complete word on both sides (a genuine one-syllable word like
        'nA'); otherwise a lone akshara coinciding is too likely by chance.
        Identical consecutive pAdas (a refrain) are skipped.
        """
        results = []
        padas = self._flatten_padas(lines)
        for (l1, p1), (l2, p2) in zip(padas, padas[1:]):
            if p1 == p2:
                continue
            a1, a2 = self.get_aksharas(p1), self.get_aksharas(p2)
            best = 0
            for k in range(min(len(a1), len(a2)), 0, -1):
                if a1[-k:] == a2[:k]:
                    best = k
                    break
            if not best:
                continue
            last_w, first_w = self._split_words(p1)[-1], self._split_words(p2)[0]
            if best < min_len:
                if not (len(self.get_aksharas(last_w)) == best
                        and len(self.get_aksharas(first_w)) == best):
                    continue
            results.append({
                "alankaram": "Muktapadagrastamu",
                "trigger": f"'{''.join(a1[-best:])}' ({best} akshara) ends '{last_w}' "
                           f"and begins '{first_w}' of the next pAda",
                "position": f"{l1} -> {l2}",
                "repeat_count": best,
            })
        return results or None