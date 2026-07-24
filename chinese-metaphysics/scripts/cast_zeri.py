#!/usr/bin/env python3
"""cast_zeri.py — almanac (通勝/黄历) layer for date selection 择日.

Prints the almanac facts for a date range and, when natal branches are
supplied, the structural interaction with the natal chart.

DESIGN RULE (matches the rest of this skill):
    This script does NOT score or rank days. It prints layers side by side.
    The almanac layer and the natal layer routinely disagree, and there is
    no canonical weighting between them. Collapsing them into one number
    would manufacture precision. Print both; let the reader see it.

KNOWN LIMITATION — almanac editions disagree:
    Published almanacs differ on 宜/忌 for the same day because they apply
    different 神煞 sets and weightings. This script reports ONE engine
    (lunar-python). Verified divergence: for 2026-07-28, lunar-python places
    开市 in 忌, while jiri123.com places it in 宜; the two also disagree on
    星宿 (尾 vs 女). Treat output as "what this engine says", not "what the
    almanac says". For a decision that matters, check a second source.

Dependency: lunar-python — already required by cast_bazi.py. No new runtime.

Usage:
    python cast_zeri.py --start 2026-07-24 --end 2026-08-06 \\
                        --natal 亥,亥,辰,巳 --activity 开市
    python cast_zeri.py --start 2026-08-03 --activity 开市 --hours
    python cast_zeri.py --start 2026-07-24 --end 2026-08-06 --json
"""
import argparse
import json
import sys
from datetime import date, timedelta

try:
    from lunar_python import Solar
except ImportError:
    sys.stderr.write(
        "ERROR: lunar-python not installed.\n"
        "  pip install lunar-python --break-system-packages\n")
    sys.exit(2)

BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未",
            "申", "酉", "戌", "亥"]

CLASH = {b: BRANCHES[(i + 6) % 12] for i, b in enumerate(BRANCHES)}

HARM = {"子": "未", "丑": "午", "寅": "巳", "卯": "辰", "辰": "卯",
        "巳": "寅", "午": "丑", "未": "子", "申": "亥", "酉": "戌",
        "戌": "酉", "亥": "申"}

SELF_PUNISH = ["辰", "午", "酉", "亥"]

MAX_RANGE_DAYS = 367


def parse_date(s, label):
    parts = str(s).strip().split("-")
    if len(parts) != 3:
        raise ValueError(f"{label} must be YYYY-MM-DD, got: {s}")
    try:
        y, m, d = (int(p) for p in parts)
        result = date(y, m, d)
    except ValueError as exc:
        raise ValueError(f"{label} is not a real date ({s}): {exc}") from exc
    if not 1900 <= y <= 2100:
        raise ValueError(f"{label} year {y} outside supported range 1900-2100")
    return result


def parse_branches(s, label):
    if not s:
        return []
    parts = [p for p in str(s).replace("，", ",").replace(" ", ",").split(",")
             if p]
    for p in parts:
        if p not in BRANCHES:
            raise ValueError(
                f'{label}: "{p}" is not an Earthly Branch. '
                f'Expected one of {"".join(BRANCHES)}')
    return parts


def natal_interaction(day_branch, natal, voids):
    """Structural relations between a day branch and the natal branches."""
    notes = []
    clash_target = CLASH[day_branch]
    n_clash = natal.count(clash_target)
    if n_clash:
        notes.append(f"冲 clashes natal {clash_target}"
                     + (f" x{n_clash}" if n_clash > 1 else ""))
    harm_target = HARM[day_branch]
    n_harm = natal.count(harm_target)
    if n_harm:
        notes.append(f"害 harms natal {harm_target}"
                     + (f" x{n_harm}" if n_harm > 1 else ""))
    if day_branch in SELF_PUNISH and day_branch in natal:
        notes.append(f"自刑 self-punish with natal {day_branch}")
    if day_branch in voids:
        notes.append("空亡 void")
    return notes


def activity_verdict(yi, ji, activity):
    if not activity:
        return None
    in_yi, in_ji = activity in yi, activity in ji
    if in_yi and in_ji:
        return "CONFLICT"
    if in_yi:
        return "宜 YES"
    if in_ji:
        return "忌 AVOID"
    return "— unlisted"


def cast_day(d, natal, voids, activity):
    lunar = Solar.fromYmd(d.year, d.month, d.day).getLunar()
    pillar = lunar.getDayInGanZhi()
    branch = lunar.getDayZhi()
    yi = list(lunar.getDayYi())
    ji = list(lunar.getDayJi())

    return {
        "date": d.isoformat(),
        "weekday": d.strftime("%a"),
        "lunar": f"{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
        "pillar": pillar,
        "branch": branch,
        "duty": lunar.getZhiXing(),
        "star28": lunar.getXiu(),
        "star28_luck": lunar.getXiuLuck(),
        "tianshen": lunar.getDayTianShen(),
        "tianshen_luck": lunar.getDayTianShenLuck(),
        "nine_star": str(lunar.getDayNineStar()),
        "jishen": list(lunar.getDayJiShen())[:10],
        "xiongsha": list(lunar.getDayXiongSha())[:10],
        "chong": lunar.getDayChongDesc(),
        "xunkong": lunar.getDayXunKong(),
        "yi": yi,
        "ji": ji,
        "natal": natal_interaction(branch, natal, voids),
        "activity": activity_verdict(yi, ji, activity),
    }


def cast_hours(d, activity, natal):
    """Hour-level 宜/忌 for the twelve 時辰."""
    out = []
    for i in range(12):
        hour = 23 if i == 0 else (i * 2 - 1)
        probe = d + timedelta(days=1) if i == 0 else d
        lunar = Solar.fromYmdHms(probe.year, probe.month, probe.day,
                                 hour, 30, 0).getLunar()
        yi = list(lunar.getTimeYi())
        ji = list(lunar.getTimeJi())
        branch = lunar.getTimeZhi()
        clash_target = CLASH[branch]
        natal_note = (f"冲 natal {clash_target}"
                      if natal.count(clash_target) else "")
        out.append({
            "cycle": lunar.getTimeInGanZhi(),
            "branch": branch,
            "range": f"{(hour if i else 23):02d}:00-{((hour + 2) % 24):02d}:00",
            "tianshen": lunar.getTimeTianShen(),
            "tianshen_luck": lunar.getTimeTianShenLuck(),
            "natal": natal_note,
            "activity": activity_verdict(yi, ji, activity),
            "yi": yi[:8],
            "ji": ji[:8],
        })
    return out


def print_day(r, activity, show_gods):
    print(f"{r['date']} {r['weekday']}  {r['pillar']}  {r['duty']}日  "
          f"{r['star28']}宿({r['star28_luck']})  "
          f"{r['tianshen']}({r['tianshen_luck']})")
    print(f"   农历{r['lunar']}   {r['chong']}   本日空亡 {r['xunkong']}")
    flags = []
    if r["activity"]:
        flags.append(f"{activity}: {r['activity']}")
    if r["natal"]:
        flags.append("NATAL: " + "; ".join(r["natal"]))
    if flags:
        print("   " + "  |  ".join(flags))
    if r["yi"]:
        print("   宜: " + " ".join(r["yi"]))
    if r["ji"]:
        print("   忌: " + " ".join(r["ji"]))
    if show_gods:
        if r["jishen"]:
            print("   吉神: " + " ".join(r["jishen"]))
        if r["xiongsha"]:
            print("   凶煞: " + " ".join(r["xiongsha"]))
    print()


def main():
    ap = argparse.ArgumentParser(
        description="Almanac layer for date selection (择日). "
                    "Prints layers; does not rank days.")
    ap.add_argument("--start", required=True, help="YYYY-MM-DD")
    ap.add_argument("--end", help="YYYY-MM-DD (default: same as start)")
    ap.add_argument("--natal", help="natal branches, e.g. 亥,亥,辰,巳")
    ap.add_argument("--void", dest="voids", help="natal void branches 空亡")
    ap.add_argument("--activity", help="activity to check, e.g. 开市")
    ap.add_argument("--hours", action="store_true",
                    help="also print the 12 時辰 (single date only)")
    ap.add_argument("--gods", action="store_true", help="also print 吉神/凶煞")
    ap.add_argument("--json", action="store_true", help="machine-readable")
    args = ap.parse_args()

    try:
        start = parse_date(args.start, "--start")
        end = parse_date(args.end, "--end") if args.end else start
        natal = parse_branches(args.natal, "--natal")
        voids = parse_branches(args.voids, "--void")
    except ValueError as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        return 2

    if end < start:
        sys.stderr.write("ERROR: --start is after --end\n")
        return 2
    span = (end - start).days + 1
    if span > MAX_RANGE_DAYS:
        sys.stderr.write(f"ERROR: range too large ({span} days, "
                         f"max {MAX_RANGE_DAYS})\n")
        return 2
    if args.hours and span > 1:
        sys.stderr.write("ERROR: --hours needs a single date (omit --end)\n")
        return 2

    days = []
    for i in range(span):
        d = start + timedelta(days=i)
        try:
            row = cast_day(d, natal, voids, args.activity)
            if args.hours:
                row["hours"] = cast_hours(d, args.activity, natal)
        except Exception as exc:
            sys.stderr.write(f"ERROR casting {d.isoformat()}: {exc}\n")
            return 3
        days.append(row)

    if args.json:
        print(json.dumps({
            "engine": "lunar-python",
            "caveat": "Almanac editions disagree on 宜/忌 and 星宿. "
                      "Single-source output.",
            "natal": natal, "voids": voids, "activity": args.activity,
            "days": days,
        }, ensure_ascii=False, indent=2))
        return 0

    print("Almanac layer — engine: lunar-python")
    if natal:
        line = f"Natal branches: {' '.join(natal)}"
        if voids:
            line += f"   void: {' '.join(voids)}"
        print(line)
    print("NOTE: almanac editions disagree on 宜/忌 and 星宿; this is one")
    print("engine's reading. Layers are printed, not scored. See docstring.\n")

    for r in days:
        print_day(r, args.activity or "activity", args.gods)
        if "hours" in r:
            print("   --- 十二時辰 ---")
            for h in r["hours"]:
                tags = []
                if h["activity"]:
                    tags.append(h["activity"])
                if h["natal"]:
                    tags.append(h["natal"])
                tag = f"  [{'; '.join(tags)}]" if tags else ""
                print(f"   {h['range']}  {h['cycle']}  "
                      f"{h['tianshen']}({h['tianshen_luck']}){tag}")
                if h["yi"]:
                    print("      宜: " + " ".join(h["yi"]))
                if h["ji"]:
                    print("      忌: " + " ".join(h["ji"]))
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
