#!/usr/bin/env python3
"""Cast a Qi Men Dun Jia (奇门遁甲) time chart (时家奇门).

Usage:
    python cast_qimen.py --datetime "2026-06-12 10:20" [--longitude 103.85] \
        [--tz-meridian 120] [--no-solar-correction] [--method 1]

Methods: 1 = 拆补 (default), 2 = 置闰. Both are real schools; see
references/methodology_forks.md.

Requires (note the ephem pin conflict is harmless -- upgrade anyway):
    pip install kinqimen --break-system-packages
    pip install --upgrade --force-reinstall ephem --break-system-packages

kinqimen 0.0.6.x has a broken internal absolute import ("import config"),
so its package directory must be added to sys.path before importing.
"""
import argparse
import sys
from datetime import datetime, timedelta


def _import_qimen():
    import importlib.util
    spec = importlib.util.find_spec("kinqimen")
    if spec is None:
        sys.exit("Missing dependency. Run:\n"
                 "  pip install kinqimen --break-system-packages\n"
                 "  pip install --upgrade --force-reinstall ephem --break-system-packages")
    import os
    pkg_dir = os.path.dirname(spec.origin)
    if pkg_dir not in sys.path:
        sys.path.insert(0, pkg_dir)  # workaround for "import config" inside the package
    try:
        from kinqimen import Qimen
    except ImportError as e:
        sys.exit(f"kinqimen import failed ({e}). If the error mentions ephem or "
                 "PyUnicode_GET_SIZE, run: pip install --upgrade --force-reinstall "
                 "ephem --break-system-packages")
    return Qimen


def solar_time_correction(clock_dt, longitude, tz_meridian=120.0):
    import math
    lon_min = (longitude - tz_meridian) * 4.0
    n = clock_dt.timetuple().tm_yday
    b = 2 * math.pi * (n - 81) / 364.0
    eot = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
    return clock_dt + timedelta(minutes=lon_min + eot)


# Luoshu layout for display: rows of (palace trigram, direction)
GRID = [[("巽", "SE"), ("離", "S"), ("坤", "SW")],
        [("震", "E"), ("中", "C"), ("兌", "W")],
        [("艮", "NE"), ("坎", "N"), ("乾", "NW")]]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--datetime", required=True, help='Local clock time "YYYY-MM-DD HH:MM"')
    ap.add_argument("--longitude", type=float, default=None)
    ap.add_argument("--tz-meridian", type=float, default=120.0)
    ap.add_argument("--no-solar-correction", action="store_true")
    ap.add_argument("--method", type=int, default=1, choices=[1, 2],
                    help="1=拆补 (default), 2=置闰")
    args = ap.parse_args()

    try:
        dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M")
    except ValueError as e:
        sys.exit(f"Bad datetime format: {e}")

    if args.longitude is not None and not args.no_solar_correction:
        corrected = solar_time_correction(dt, args.longitude, args.tz_meridian)
        print(f"Clock {dt} -> solar time {corrected.strftime('%Y-%m-%d %H:%M')}")
        dt = corrected

    Qimen = _import_qimen()
    try:
        pan = Qimen(dt.year, dt.month, dt.day, dt.hour, dt.minute).pan(args.method)
    except Exception as e:
        sys.exit(f"Casting failed: {e}")

    print(f"\n干支: {pan['干支']}")
    print(f"局: {pan['排局']} | 节气: {pan['節氣']} | 排盘: {pan['排盤方式']}")
    print(f"旬首: {pan['旬首']} | 旬空: 日空 {pan['旬空']['日空']} / 时空 {pan['旬空']['時空']}")
    zs = pan["值符值使"]
    print(f"值符: 星{zs['值符星宮'][0]} 落{zs['值符星宮'][1]}宫 | "
          f"值使: 门{zs['值使門宮'][0]} 落{zs['值使門宮'][1]}宫")
    print(f"马星: {pan['馬星']}\n")

    tian, di = pan["天盤"], pan["地盤"]
    men, xing, shen = pan["門"], pan["星"], pan["神"]
    for row in GRID:
        cells = []
        for trigram, direction in row:
            t = tian.get(trigram, "")
            t = "".join(t) if isinstance(t, (list, tuple)) else t
            cells.append(f"{trigram}({direction}): 神{shen.get(trigram, '-')} "
                         f"星{xing.get(trigram, '-')} 门{men.get(trigram, '-')} "
                         f"天[{t}] 地[{di.get(trigram, '-')}]")
        print(" | ".join(f"{c:<38}" for c in cells))
    print("\n(中宫 center: 天[{}] 地[{}])".format(tian.get("中", "-"), di.get("中", "-")))


if __name__ == "__main__":
    main()
