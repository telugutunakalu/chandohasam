"""
PoemMetrics — poem-level measures built on AlankaramChecker's phoneme parsing.

    1. alliteration_density : how much consonant repetition (anuprAsa of any
                              kind, phonetic equivalents folded together)
    2. euphony_index        : mAdhurya — weighted softness/harshness of the
                              consonants, averaged over the poem

All phoneme labels are the Harvard-Kyoto ones used in alankaram_checker.py
(z = ś, S = ṣ, G = ṅ, J = ñ, T/D/N = retroflex, L = ళ, R = ఱ, M = anusvāra).

Sources for the euphony weights are given next to the tables below. The
classical texts state categorical rules, not numbers, so the numeric
magnitudes are this implementation's operationalisation; every one of them
can be overridden through `weights=` / `cluster_penalties=`.
"""
from collections import Counter

from alankaras import AlankaramChecker


class PoemMetrics:
    NASALS = {'G', 'J', 'N', 'n', 'm'}
    SONORANTS = {'y', 'v', 'l', 'L'}

    # Homorganic nasal -> stops of its own varga. The ṭavarga is deliberately
    # absent: Kāvyaprakāśa's mādhurya sūtra says "aṭavargāḥ" (not the ṭa-varga).
    HOMORGANIC = {
        'G': {'k', 'kh', 'g', 'gh'},
        'J': {'c', 'ch', 'j', 'jh'},
        'n': {'t', 'th', 'd', 'dh'},
        'm': {'p', 'ph', 'b', 'bh'},
    }

    # r, R, N count as soft only as a lone consonant before a SHORT vowel
    # (Kāvyaprakāśa 8: "raṇau laghū", read this way by Sandhan et al. 2023).
    CONDITIONAL_SOFT = {'r', 'R', 'N'}

    DEFAULT_WEIGHTS = {
        # --- soft (mādhurya) --------------------------------------------
        # nasals of the varga, incl. anusvāra/arasunna: the core mādhurya
        # letters (Kāvyaprakāśa 8; Vāmana); Fónagy 1961: sonorants in tender poems
        'G': 1.0, 'J': 1.0, 'n': 1.0, 'm': 1.0, 'M': 1.0,
        # conditional: applied only under the short-vowel rule above
        'r': 1.0, 'R': 1.0, 'N': 1.0,
        # semivowels/liquids: not named in the mādhurya sūtra; supported by
        # the sonorant finding (Fónagy 1961) and by your spec -> weaker
        'y': 0.5, 'v': 0.5, 'l': 0.5, 'L': 0.5,
        # unaspirated non-retroflex stops: the varga sparśas the sūtra allows
        'k': 0.25, 'g': 0.25, 'c': 0.25, 'j': 0.25,
        't': 0.25, 'd': 0.25, 'p': 0.25, 'b': 0.25,
        # --- mildly hard --------------------------------------------------
        # aspirates: the ojas sūtra singles out aspirate conjuncts; alone they
        # are just "not unaspirated" -> mild
        'kh': -0.25, 'gh': -0.25, 'ch': -0.25, 'jh': -0.25,
        'th': -0.25, 'dh': -0.25, 'ph': -0.25, 'bh': -0.25,
        # dental s: hissing fricatives go with high-arousal negative words
        # (Adelman et al. 2018); not in the ojas sūtra itself -> mild
        's': -0.5,
        # --- hard (ojas) --------------------------------------------------
        # ṭavarga stops (excluded from mādhurya; "ṭādiḥ" heads the ojas list)
        'T': -1.0, 'Th': -1.0, 'D': -1.0, 'Dh': -1.0,
        # ś and ṣ ("śaṣau" in the ojas sūtra)
        'z': -1.0, 'S': -1.0,
        # --- neutral ------------------------------------------------------
        'h': 0.0, 'H': 0.0,
    }

    # Consonant clusters: Vāmana/Mammaṭa tie gauḍī/ojas to many saṃyuktākṣara.
    # Per the ojas sūtra (Sandhan et al. 2023's reading): a consonant with r,
    # a consonant with itself, and the like.
    DEFAULT_CLUSTER_PENALTIES = {'geminate': -1.0, 'r': -1.0, 'other': -0.5}

    def __init__(self, checker=None, weights=None, cluster_penalties=None,
                 penalize_soft_geminates=False):
        """
        weights                   overrides for DEFAULT_WEIGHTS (per HK label)
        cluster_penalties         overrides for DEFAULT_CLUSTER_PENALTIES
        penalize_soft_geminates   the ojas rule "a consonant with itself" is
                                  read literally if True. Default False: nasal
                                  and semivowel geminates (అమ్మ, వెన్నెల) are
                                  exempt, since the same tradition ranks nasals
                                  as the softest letters. This exemption is a
                                  judgment call, not something I could verify
                                  in the sūtra text.
        """
        self.checker = checker or AlankaramChecker()
        self.w = {**self.DEFAULT_WEIGHTS, **(weights or {})}
        self.cluster = {**self.DEFAULT_CLUSTER_PENALTIES, **(cluster_penalties or {})}
        self.penalize_soft_geminates = penalize_soft_geminates

    # ------------------------------------------------------------ helpers
    @staticmethod
    def _short_vowels(script):
        # Telugu/HK e, o are short (E, O long). In Devanagari/Sanskrit e, o are
        # inherently long. ai/au are always long.
        short = {'a', 'i', 'u', 'R', 'lR'}
        if script != 'devanagari':
            short |= {'e', 'o'}
        return short

    def _cluster_penalty(self, onset):
        """Penalty for one akshara's consonant cluster, or None if it carries none."""
        if len(onset) < 2:
            return None
        if len(onset) == 2 and onset[1] in self.HOMORGANIC.get(onset[0], ()):
            return None                       # nasal + own-varga stop: a mādhurya conjunct
        if len(set(onset)) == 1:              # geminate
            c = onset[0]
            if not self.penalize_soft_geminates and (c in self.NASALS or c in self.SONORANTS):
                return None
            return self.cluster['geminate']
        if any(c in ('r', 'R') for c in onset):
            return self.cluster['r']
        return self.cluster['other']

    def _line_weights(self, line):
        """(weights, n_aksharas, n_cluster_events) for one pAda."""
        short = self._short_vowels(self.checker.detect_script(line))
        weights, n_aksharas, n_clusters = [], 0, 0
        for ak in self.checker.parse_aksharas(line):
            onset, vowel, coda = ak['onset'], ak['vowel'], ak['coda']
            n_aksharas += 1
            lone = len(onset) == 1
            for c in onset:
                if c in self.CONDITIONAL_SOFT:
                    weights.append(self.w.get(c, 0.0) if (lone and vowel in short) else 0.0)
                else:
                    weights.append(self.w.get(c, 0.0))
            for m in coda:                    # anusvāra / arasunna / visarga
                weights.append(self.w.get(m, 0.0))
            pen = self._cluster_penalty(onset)
            if pen is not None:
                weights.append(pen)
                n_clusters += 1
        return weights, n_aksharas, n_clusters

    # ------------------------------------------------------ 2. euphony index
    def euphony_index(self, lines):
        """
        Mādhurya ("sweetness") index: the mean weight of the poem's sound
        events, in [-1, +1] (+1 all-soft, 0 neutral, -1 all-hard). Events are
        consonants, anusvāra/visarga, and one event per non-mādhurya
        consonant cluster (weighted by DEFAULT_CLUSTER_PENALTIES), so "few
        clusters" is part of the score itself. Vowels carry no weight, except
        that vowel length gates the soft weight of r / R / N.

        Returns None if there are no sound events.
        """
        all_w, per_line = [], []
        n_ak = n_cl = 0
        for label, pada in self.checker._flatten_padas(lines):
            w, a, c = self._line_weights(pada)
            all_w += w
            n_ak += a
            n_cl += c
            per_line.append({"position": label, "tokens": len(w),
                             "euphony_index": sum(w) / len(w) if w else None})
        if not all_w:
            return None
        n = len(all_w)
        return {
            "euphony_index": sum(all_w) / n,
            "soft_share": sum(x > 0 for x in all_w) / n,
            "neutral_share": sum(x == 0 for x in all_w) / n,
            "harsh_share": sum(x < 0 for x in all_w) / n,
            "cluster_events": n_cl,
            "cluster_rate": n_cl / n_ak if n_ak else 0.0,   # per akshara
            "tokens": n,
            "per_line": per_line,
        }

    # ------------------------------------------------ 1. alliteration density

    # Phonetic equivalents folded together before counting repeats.
    # Aspirates -> unaspirated, all sibilants -> s, ళ -> l, ఱ -> r.
    # Retroflex vs dental stops are kept distinct. Override through `fold=`.
    DEFAULT_FOLD = {
        'kh': 'k', 'gh': 'g', 'ch': 'c', 'jh': 'j',
        'th': 't', 'dh': 'd', 'ph': 'p', 'bh': 'b',
        'Th': 'T', 'Dh': 'D',
        'z': 's', 'S': 's',
        'L': 'l', 'R': 'r',
    }
    NON_CONSONANTS = {'M', 'H'}   # anusvāra / visarga

    # ------------------------------------------------ 1. alliteration density
    def alliteration_density(self, lines, max_n=3, fold=None):
        """
        Character-weighted repetition density over the poem's consonants.

        Every consonant sequence of length n (1..max_n) that occurs c > 1
        times adds n * (c - 1). The total is divided by the number of
        consonants, so longer repeated sequences weigh more. Sequences are
        built inside a single pAda (they never span a line break) and are
        counted across the whole poem. Vowels are skipped, so a sequence is a
        run of consecutive consonants in the pAda.

        Returns None if there are no consonants.
        """
        fold_map = {**self.DEFAULT_FOLD, **(fold or {})}
        counts = {n: Counter() for n in range(1, max_n + 1)}
        per_line, total = [], 0

        for label, pada in self.checker._flatten_padas(lines):
            cons = []
            for ak in self.checker.parse_aksharas(pada):
                for c in list(ak['onset']) + list(ak['coda']):
                    if c not in self.NON_CONSONANTS:
                        cons.append(fold_map.get(c, c))
            total += len(cons)
            per_line.append({"position": label, "consonants": len(cons)})
            for n in counts:
                counts[n].update(tuple(cons[i:i + n])
                                 for i in range(len(cons) - n + 1))

        if not total:
            return None

        by_length = {n: sum(n * (c - 1) for c in cnt.values() if c > 1)
                     for n, cnt in counts.items()}
        top = sorted(((seq, c) for cnt in counts.values()
                      for seq, c in cnt.items() if c > 1),
                     key=lambda x: (-len(x[0]) * (x[1] - 1), x[0]))[:5]
        return {
            "alliteration_density": sum(by_length.values()) / total,
            "by_length": {n: v / total for n, v in by_length.items()},
            "top_repeats": [("".join(s), c) for s, c in top],
            "consonants": total,
            "per_line": per_line,
        }