#!/usr/bin/env python3
"""Cast a Zi Wei Dou Shu (Purple Star) 12-palace chart.

Usage:
    python cast_ziwei.py --date 2000-05-05 --time 23:20 --longitude 103.85 \
        --gender female [--no-solar-correction] [--time-index N]

If --time-index is given (0=early-zi .. 11=hai, 12=late-zi), it is used
directly. Otherwise the index is derived from --time, with true-solar-time
correction when --longitude is provided.

Requires: pip install py-iztro --break-system-packages
"""
import argparse
import sys
from datetime import datetime, timedelta

try:
    from py_iztro import Astro
except ImportError:
    sys.exit("Missing dependency. Run: pip install py-iztro --break-system-packages")

# Life-lord by YEAR BRANCH (one school; py-iztro itself uses the
# life-palace-branch school -- see references/methodology_forks.md)
MINGZHU_BY_YEAR_BRANCH = {"子": "贪狼", "丑": "巨门", "亥": "巨门", "寅": "禄存",
                          "戌": "禄存", "卯": "文曲", "酉": "文曲", "辰": "廉贞",
                          "申": "廉贞", "巳": "武曲", "未": "武曲", "午": "破军"}


def hour_to_index(dt):
    """Map a datetime to iztro time index: 0 = 00:00-00:59 early zi, 1 = chou
    (01:00-02:59) ... 11 = hai (21:00-22:59), 12 = late zi (23:00-23:59)."""
    h = dt.hour
    if h == 0:
        return 0
    if h == 23:
        return 12
    return (h + 1) // 2


def solar_time_correction(clock_dt, longitude, tz_meridian=120.0):
    import math
    lon_min = (longitude - tz_meridian) * 4.0
    n = clock_dt.timetuple().tm_yday
    b = 2 * math.pi * (n - 81) / 364.0
    eot = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
    return clock_dt + timedelta(minutes=lon_min + eot)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", required=True, help="Birth date YYYY-MM-DD (local clock)")
    ap.add_argument("--time", help="Birth time HH:MM (local clock)")
    ap.add_argument("--time-index", type=int, choices=range(13),
                    help="Direct iztro time index 0-12 (overrides --time)")
    ap.add_argument("--longitude", type=float, default=None)
    ap.add_argument("--tz-meridian", type=float, default=120.0)
    ap.add_argument("--gender", choices=["male", "female"], required=True)
    ap.add_argument("--no-solar-correction", action="store_true")
    args = ap.parse_args()

    if args.time_index is not None:
        idx = args.time_index
        date_for_cast = args.date
    elif args.time:
        try:
            clock = datetime.strptime(f"{args.date} {args.time}", "%Y-%m-%d %H:%M")
        except ValueError as e:
            sys.exit(f"Bad date/time format: {e}")
        dt = clock
        if args.longitude is not None and not args.no_solar_correction:
            dt = solar_time_correction(clock, args.longitude, args.tz_meridian)
            print(f"Clock {clock} -> solar time {dt.strftime('%Y-%m-%d %H:%M')}")
        idx = hour_to_index(dt)
        date_for_cast = dt.strftime("%Y-%m-%d")  # solar correction can shift the date
    else:
        sys.exit("Provide --time or --time-index")

    gender = "女" if args.gender == "female" else "男"
    try:
        chart = Astro().by_solar(date_for_cast.replace("-0", "-"), idx, gender)
    except Exception as e:
        sys.exit(f"Casting failed for {date_for_cast} index {idx}: {e}")

    print(f"\nSolar {chart.solar_date} | Lunar {chart.lunar_date} | {chart.chinese_date}")
    print(f"Bureau (五行局): {chart.five_elements_class}")
    year_branch = chart.chinese_date.split(" ")[0][1]
    print(f"Life lord (命主): {chart.soul} [life-palace school] / "
          f"{MINGZHU_BY_YEAR_BRANCH.get(year_branch, '?')} [year-branch school]")
    print(f"Body lord (身主): {chart.body}\n")

    header = f"{'Palace':<10}{'GZ':<6}{'Decade':<10}{'Stars':<46}{'Body'}"
    print(header)
    print("-" * len(header))
    for p in chart.palaces:
        majors = " ".join(f"{s.name}{('化' + s.mutagen) if s.mutagen else ''}"
                          for s in p.major_stars)
        minors = " ".join(s.name for s in p.minor_stars)
        stars = (majors + (" | " + minors if minors else "")) or "(borrows opposite)"
        decade = f"{p.decadal.range[0]}-{p.decadal.range[1]}"
        body = "身宮" if p.is_body_palace else ""
        gz = f"{p.heavenly_stem}{p.earthly_branch}"
        print(f"{p.name:<10}{gz:<6}{decade:<10}{stars:<46}{body}")

    # Decade flying transformations (大限四化): each decade-palace stem fires
    # its own four transformations onto the natal stars.
    SIHUA = {"甲": "廉贞,破军,武曲,太阳", "乙": "天机,天梁,紫微,太阴",
             "丙": "天同,天机,文昌,廉贞", "丁": "太阴,天同,天机,巨门",
             "戊": "贪狼,太阴,右弼,天机", "己": "武曲,贪狼,天梁,文曲",
             "庚": "太阳,武曲,太阴,天同", "辛": "巨门,太阳,文曲,文昌",
             "壬": "天梁,紫微,左辅,武曲", "癸": "破军,巨门,太阴,贪狼"}
    star_palace = {}
    for p in chart.palaces:
        for s in list(p.major_stars) + list(p.minor_stars):
            star_palace[s.name] = p.name
    print("\nDecade four transformations (大限四化) -- 禄/权/科/忌 by decade stem:")
    for p in sorted(chart.palaces, key=lambda x: x.decadal.range[0]):
        stars4 = SIHUA[p.heavenly_stem].split(",")
        landed = " ".join(f"{lab}:{st}@{star_palace.get(st, '?')}"
                          for lab, st in zip(["禄", "权", "科", "忌"], stars4))
        print(f"  {p.decadal.range[0]:>3}-{p.decadal.range[1]:<3} ({p.heavenly_stem}"
              f"{p.earthly_branch} {p.name}): {landed}")


if __name__ == "__main__":
    main()
