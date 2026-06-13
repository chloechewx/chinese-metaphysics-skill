#!/usr/bin/env python3
"""Check a candidate person's zodiac branch against ALL natal branches.

Prevents the classic compatibility-reading error of checking only one
anchor branch (e.g. ranking a sign as ideal via the day branch while
missing its clash with the year branch).

Usage:
    python check_compat.py --natal 辰 巳 亥 亥 --void 子丑 --candidate 寅
    python check_compat.py --natal 辰 巳 亥 亥 --void 子丑 --all

--natal takes the four branches in order: year month day hour.
--void takes the day-pillar void pair (printed by cast_bazi.py as 空亡).
--all evaluates every one of the 12 branches and prints a ranked summary.
"""
import argparse
import sys

BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
ANIMALS = dict(zip(BRANCHES, ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
                              "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]))
PILLAR_NAMES = ["year (social/zodiac)", "month (career env)",
                "day (spouse palace)", "hour (inner/later life)"]

SIX_COMBO = {frozenset(p) for p in ["子丑", "寅亥", "卯戌", "辰酉", "巳申", "午未"]}
CLASH = {frozenset(p) for p in ["子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥"]}
HARM = {frozenset(p) for p in ["子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌"]}
TRINES = [set("申子辰"), set("亥卯未"), set("寅午戌"), set("巳酉丑")]
PUNISH_GROUPS = [set("寅巳申"), set("丑未戌")]
PUNISH_PAIR = {frozenset("子卯")}
SELF_PUNISH = set("辰午酉亥")

SCORE = {"六合": 3, "三合": 2, "冲": -3, "刑": -2, "自刑": -2, "害": -1}


def interactions(candidate, natal):
    """Return list of (relation, natal_branch, pillar_index)."""
    out = []
    for i, nb in enumerate(natal):
        pair = frozenset({candidate, nb})
        if pair in SIX_COMBO:
            out.append(("六合", nb, i))
        if pair in CLASH:
            out.append(("冲", nb, i))
        if pair in HARM:
            out.append(("害", nb, i))
        if candidate != nb and any({candidate, nb} <= t for t in TRINES):
            out.append(("三合", nb, i))
        if (pair in PUNISH_PAIR
                or (candidate != nb and any({candidate, nb} <= g for g in PUNISH_GROUPS))):
            out.append(("刑", nb, i))
        if candidate == nb and candidate in SELF_PUNISH:
            out.append(("自刑", nb, i))
    return out


def evaluate(candidate, natal, void):
    rels = interactions(candidate, natal)
    score = sum(SCORE[r] for r, _, _ in rels)
    is_void = candidate in void
    return rels, score, is_void


def report(candidate, natal, void):
    rels, score, is_void = evaluate(candidate, natal, void)
    print(f"\nCandidate: {candidate} ({ANIMALS[candidate]})  net score: {score:+d}"
          f"{'  [VOID branch -- connection may feel hollow/delayed]' if is_void else ''}")
    if not rels:
        print("  No direct interactions with any natal branch (neutral).")
    for r, nb, i in rels:
        print(f"  {candidate}{nb}{r}  with natal {PILLAR_NAMES[i]}")
    print("  NOTE: net score is a screening aid; weight 冲/刑 on the palace "
          "relevant to the question (spouse palace for romance, etc.) above "
          "the raw total, and read mixed results as 'strong but with a cost'.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--natal", nargs=4, required=True,
                    metavar=("YEAR", "MONTH", "DAY", "HOUR"))
    ap.add_argument("--void", default="", help="Day-pillar void pair, e.g. 子丑")
    ap.add_argument("--candidate", help="Single branch to evaluate")
    ap.add_argument("--all", action="store_true", help="Rank all 12 branches")
    args = ap.parse_args()

    for b in args.natal + list(args.void) + ([args.candidate] if args.candidate else []):
        if b not in BRANCHES:
            sys.exit(f"'{b}' is not a valid earthly branch ({''.join(BRANCHES)})")

    if args.candidate:
        report(args.candidate, args.natal, args.void)
    elif args.all:
        ranked = sorted(BRANCHES,
                        key=lambda c: evaluate(c, args.natal, args.void)[1],
                        reverse=True)
        print(f"Natal: {' '.join(args.natal)} | Void: {args.void or '(none given)'}")
        for c in ranked:
            rels, score, is_void = evaluate(c, args.natal, args.void)
            tags = ",".join(f"{r}@{PILLAR_NAMES[i].split()[0]}" for r, _, i in rels) or "neutral"
            flag = " VOID" if is_void else ""
            print(f"  {score:+3d}  {c} {ANIMALS[c]:<8} {tags}{flag}")
    else:
        sys.exit("Provide --candidate or --all")


if __name__ == "__main__":
    main()
