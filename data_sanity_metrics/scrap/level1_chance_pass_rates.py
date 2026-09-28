"""Level 1 (sense check) — how often would the prāsa and yati checks pass by chance?

"100% prosodic integrity" is informative only in proportion to how hard each
rule is to satisfy. This script estimates each rule's chance pass rate under
the paper's own analyser (dwipada_analyser) by pairing aksharas from
*unrelated* lines of the master corpus:

    yati   foot-1 akshara of line i  vs  foot-3 akshara of a random line j
           (full cascade; then without the svara-yati fallback, i.e. vowel-only
           matching when the consonants are not in maitri)
    prāsa  line 1 of couplet i  vs  line 2 of a random couplet j

Real (aligned) pairs are scored the same way for comparison. A rule whose
chance rate is near its real rate cannot certify much.

Writes outputs/level1_chance_pass_rates.json

Run:  python level1_chance_pass_rates.py
"""
import random
from collections import Counter

import config
from common.dataset import load_subset, poem_lines
from common.io import pct, print_table, save_result
from common.scanners import _paper_module

da = _paper_module()


def yati_rule(first, third, svara=True):
    """Which rule (if any) accepts the pair, following the analyser's cascade
    (_resolve_yati_for_line): maitri, then svara, samyukta, bindu yati.
    svara=False drops the vowel-only fallback and keeps the rest."""
    if not (first["first_letter"] and third["third_gana_first_letter"]):
        return None
    match, _, details = da.check_yati_maitri(first["first_letter"], third["third_gana_first_letter"])
    if match:
        return details.get("match_type", "maitri")
    a1, a3 = first["first_aksharam"], third["third_gana_first_aksharam"]
    if not (a1 and a3):
        return "no_match"
    if svara and da.check_svara_yati(a1, a3):
        return "svara_yati"
    if da.check_samyukta_yati(a1, a3):
        return "samyukta_yati"
    if da.check_bindu_yati(a1, a3):
        return "bindu_yati"
    return "no_match"


def rates(pairs, svara):
    rules = Counter(yati_rule(a, b, svara) for a, b in pairs)
    rules.pop(None, None)
    n = sum(rules.values())
    return {"n": n, "pass_pct": pct(n - rules.get("no_match", 0), n),
            "by_rule_pct": {k: pct(v, n) for k, v in rules.most_common()}}


def main():
    master = load_subset("master")
    rng = random.Random(config.SEED)
    padas = [da.analyze_pada(l) for r in master for l in poem_lines(r)]
    perm = list(range(len(padas)))
    rng.shuffle(perm)

    real_yati = [(p, p) for p in padas]
    chance_yati = [(padas[i], padas[j]) for i, j in enumerate(perm) if i != j]

    yati = {
        "real_full": rates(real_yati, True),
        "chance_full": rates(chance_yati, True),
        "real_no_svara": rates(real_yati, False),
        "chance_no_svara": rates(chance_yati, False),
    }
    print("Yati pass rate, paper analyser (per line)")
    print_table(["pairing", "cascade", "pass %"],
                [["real", "full (paper)", yati["real_full"]["pass_pct"]],
                 ["chance", "full (paper)", yati["chance_full"]["pass_pct"]],
                 ["real", "no svara-yati", yati["real_no_svara"]["pass_pct"]],
                 ["chance", "no svara-yati", yati["chance_no_svara"]["pass_pct"]]])
    print("\nchance pairs, full cascade, accepted by rule (%):", yati["chance_full"]["by_rule_pct"])

    # prāsa: line 1 of couplet i vs line 2 of couplet j
    l1 = [poem_lines(r)[0] for r in master]
    l2 = [poem_lines(r)[1] for r in master]
    cperm = list(range(len(master)))
    rng.shuffle(cperm)
    real_prasa = sum(da.check_prasa(a, b)[0] for a, b in zip(l1, l2))
    chance_prasa = sum(da.check_prasa(l1[i], l2[j])[0] for i, j in enumerate(cperm) if i != j)
    n_chance = sum(1 for i, j in enumerate(cperm) if i != j)
    prasa = {"real_pass_pct": pct(real_prasa, len(master)), "chance_pass_pct": pct(chance_prasa, n_chance)}
    print(f"\nPrāsa pass rate: real {prasa['real_pass_pct']:.1f}%, chance {prasa['chance_pass_pct']:.1f}%")

    # whole-couplet chance: both yati lines and prāsa by chance (independence approximation)
    y = yati["chance_full"]["pass_pct"] / 100
    p = prasa["chance_pass_pct"] / 100
    both = 100 * y * y * p
    print(f"chance that a random couplet satisfies prāsa + both yati (given a valid gaṇa frame): ~{both:.1f}%")

    save_result("level1_chance_pass_rates", {"yati": yati, "prasa": prasa,
                                             "chance_couplet_prasa_and_yati_pct": both})


if __name__ == "__main__":
    main()
