#!/usr/bin/env python3
"""Cast a BaZi (Four Pillars) chart with true-solar-time correction.

Usage:
    python cast_bazi.py --date 2000-05-05 --time 23:20 --longitude 103.85 \
        --gender female [--no-solar-correction] [--year YYYY]

Outputs: corrected time, four pillars (plus clock-time variant if it differs),
hidden stems, ten gods, nayin, void branches, branch interactions, shensha,
luck pillars (da yun), and the annual pillar for --year (default: current year).

Requires: pip install lunar-python --break-system-packages
"""
import argparse
import sys
from datetime import datetime, timedelta

try:
    from lunar_python import Solar
except ImportError:
    sys.exit("Missing dependency. Run: pip install lunar-python --break-system-packages")

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
STEM_ELEMENT = dict(zip(STEMS, ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]))
STEM_YANG = {s: i % 2 == 0 for i, s in enumerate(STEMS)}
# Element generation cycle: wood -> fire -> earth -> metal -> water -> wood
GEN = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CTRL = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


def ten_god(day_stem, other_stem):
    """Ten-god relationship of other_stem relative to the day master."""
    de, oe = STEM_ELEMENT[day_stem], STEM_ELEMENT[other_stem]
    same_polarity = STEM_YANG[day_stem] == STEM_YANG[other_stem]
    if oe == de:
        return "比肩" if same_polarity else "劫财"
    if GEN[de] == oe:
        return "食神" if same_polarity else "伤官"
    if CTRL[de] == oe:
        return "偏财" if same_polarity else "正财"
    if CTRL[oe] == de:
        return "七杀" if same_polarity else "正官"
    if GEN[oe] == de:
        return "偏印" if same_polarity else "正印"
    return "?"


# --- Branch interactions ---
CLASHES = [set(p) for p in ["子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥"]]
SIX_COMBOS = [set(p) for p in ["子丑", "寅亥", "卯戌", "辰酉", "巳申", "午未"]]
HARMS = [set(p) for p in ["子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌"]]
SELF_PUNISH = set("辰午酉亥")
PUNISH_GROUPS = [set("寅巳申"), set("丑未戌")]
PUNISH_PAIR = [set("子卯")]


def branch_interactions(branches):
    found = []
    n = len(branches)
    for i in range(n):
        for j in range(i + 1, n):
            pair = {branches[i], branches[j]}
            tag = f"{branches[i]}{branches[j]}"
            if pair in CLASHES:
                found.append(f"{tag}冲 (clash, pillars {i+1}&{j+1})")
            if pair in SIX_COMBOS:
                found.append(f"{tag}合 (combination, pillars {i+1}&{j+1})")
            if pair in HARMS:
                found.append(f"{tag}害 (harm, pillars {i+1}&{j+1})")
            if pair in PUNISH_PAIR or (len(pair) == 2 and any(pair <= g for g in PUNISH_GROUPS)):
                found.append(f"{tag}刑 (punishment, pillars {i+1}&{j+1})")
            if branches[i] == branches[j] and branches[i] in SELF_PUNISH:
                found.append(f"{branches[i]}{branches[j]}自刑 (self-punishment, pillars {i+1}&{j+1})")
    return found


# --- Shensha (symbolic stars). Keys are the reference point noted per table. ---
TIANYI = {"甲": "丑未", "戊": "丑未", "庚": "丑未", "乙": "子申", "己": "子申",
          "丙": "亥酉", "丁": "亥酉", "壬": "卯巳", "癸": "卯巳", "辛": "午寅"}
YUEDE = {"寅": "丙", "午": "丙", "戌": "丙", "申": "壬", "子": "壬", "辰": "壬",
         "亥": "甲", "卯": "甲", "未": "甲", "巳": "庚", "酉": "庚", "丑": "庚"}
TIANDE = {"寅": "丁", "卯": "申", "辰": "壬", "巳": "辛", "午": "亥", "未": "甲",
          "申": "癸", "酉": "寅", "戌": "丙", "亥": "乙", "子": "巳", "丑": "庚"}
HUAGAI = {"寅": "戌", "午": "戌", "戌": "戌", "申": "辰", "子": "辰", "辰": "辰",
          "巳": "丑", "酉": "丑", "丑": "丑", "亥": "未", "卯": "未", "未": "未"}
YIMA = {"寅": "申", "午": "申", "戌": "申", "申": "寅", "子": "寅", "辰": "寅",
        "巳": "亥", "酉": "亥", "丑": "亥", "亥": "巳", "卯": "巳", "未": "巳"}
TAOHUA = {"寅": "卯", "午": "卯", "戌": "卯", "申": "酉", "子": "酉", "辰": "酉",
          "巳": "午", "酉": "午", "丑": "午", "亥": "子", "卯": "子", "未": "子"}
JIESHA = {"申": "巳", "子": "巳", "辰": "巳", "寅": "亥", "午": "亥", "戌": "亥",
          "巳": "寅", "酉": "寅", "丑": "寅", "亥": "申", "卯": "申", "未": "申"}
WANGSHEN = {"寅": "巳", "午": "巳", "戌": "巳", "申": "亥", "子": "亥", "辰": "亥",
            "巳": "申", "酉": "申", "丑": "申", "亥": "寅", "卯": "寅", "未": "寅"}
GUCHEN = {"亥": "寅", "子": "寅", "丑": "寅", "寅": "巳", "卯": "巳", "辰": "巳",
          "巳": "申", "午": "申", "未": "申", "申": "亥", "酉": "亥", "戌": "亥"}
GUASU = {"亥": "戌", "子": "戌", "丑": "戌", "寅": "丑", "卯": "丑", "辰": "丑",
         "巳": "辰", "午": "辰", "未": "辰", "申": "未", "酉": "未", "戌": "未"}
TIANYI_DOC = {"寅": "丑", "卯": "寅", "辰": "卯", "巳": "辰", "午": "巳", "未": "午",
              "申": "未", "酉": "申", "戌": "酉", "亥": "戌", "子": "亥", "丑": "子"}
YINCHAYANGCUO = {"丙子", "丁丑", "戊寅", "辛卯", "壬辰", "癸巳",
                 "丙午", "丁未", "戊申", "辛酉", "壬戌", "癸亥"}
SHIEDABAI = {"甲辰", "乙巳", "丙申", "丁亥", "戊戌", "己丑", "庚辰", "辛巳", "壬申", "癸亥"}


def shensha(pillars_gz):
    """pillars_gz: list of 4 ganzhi strings [year, month, day, hour]."""
    yg, mg, dg, hg = pillars_gz
    stems = [p[0] for p in pillars_gz]
    branches = [p[1] for p in pillars_gz]
    day_stem, year_branch, month_branch, day_gz = dg[0], yg[1], mg[1], dg
    out = []
    hits = [b for b in branches if b in TIANYI.get(day_stem, "")]
    if hits:
        out.append(f"天乙贵人 (Nobleman) at {','.join(hits)}")
    if YUEDE.get(month_branch) in stems:
        out.append(f"月德贵人 (Monthly Virtue): stem {YUEDE[month_branch]}")
    td = TIANDE.get(month_branch)
    if td in stems or td in branches:
        out.append(f"天德贵人 (Heavenly Virtue): {td}")
    for name, table, ref in [("华盖 (Flowery Canopy)", HUAGAI, year_branch),
                             ("驿马 (Travel Horse)", YIMA, year_branch),
                             ("桃花 (Peach Blossom)", TAOHUA, year_branch),
                             ("劫煞 (Robbery)", JIESHA, year_branch),
                             ("亡神 (Vanishing Spirit)", WANGSHEN, year_branch),
                             ("孤辰 (Solitary)", GUCHEN, year_branch),
                             ("寡宿 (Lonesome)", GUASU, year_branch),
                             ("天医 (Heavenly Doctor)", TIANYI_DOC, month_branch)]:
        target = table.get(ref)
        if target in branches:
            out.append(f"{name} at {target}")
    if day_gz in YINCHAYANGCUO:
        out.append(f"阴差阳错 day ({day_gz}): relationship-dissonance flag")
    if day_gz in SHIEDABAI:
        out.append(f"十恶大败 day ({day_gz}): thin effort-reward flag")
    return out


# --- Stem five-combinations (五合) ---
WUHE = {frozenset("甲己"): "土", frozenset("乙庚"): "金", frozenset("丙辛"): "水",
        frozenset("丁壬"): "木", frozenset("戊癸"): "火"}

BRANCH_ELEMENT = {"寅": "木", "卯": "木", "巳": "火", "午": "火", "申": "金",
                  "酉": "金", "亥": "水", "子": "水", "辰": "土", "戌": "土",
                  "丑": "土", "未": "土"}


def season_state(dm_element, month_branch):
    """旺相休囚死 state of the Day Master in its birth month."""
    me = BRANCH_ELEMENT[month_branch]
    if me == dm_element:
        return "旺"
    if GEN[me] == dm_element:
        return "相"
    if GEN[dm_element] == me:
        return "休"
    if CTRL[dm_element] == me:
        return "囚"
    return "死"


def branch_damage_factors(branches):
    """Per-pillar damage multiplier from clashes/punishments/harms among
    the natal branches. Clashed or punished roots count for less."""
    f = [1.0, 1.0, 1.0, 1.0]
    n = len(branches)
    for i in range(n):
        for j in range(i + 1, n):
            pair = {branches[i], branches[j]}
            if pair in CLASHES:
                f[i] *= 0.5
                f[j] *= 0.5
            if branches[i] == branches[j] and branches[i] in SELF_PUNISH:
                f[i] *= 0.6
                f[j] *= 0.6
            if pair in HARMS:
                f[i] *= 0.85
                f[j] *= 0.85
            if (pair in PUNISH_PAIR
                    or (len(pair) == 2 and any(pair <= g for g in PUNISH_GROUPS))):
                f[i] *= 0.8
                f[j] *= 0.8
    return f


def strength_analysis(ec):
    """Transparent heuristic Day Master strength score.

    Support = peer + resource elements; Oppose = output + wealth + officer.
    Hidden-stem weights 10/5/3 by position; month branch doubled; roots
    multiplied by damage factors; season state adds a fixed component.
    Verdict has an explicit BORDERLINE band (43-57%) because legitimate
    schools weight these inputs differently -- see methodology_forks.md.
    """
    dm = ec.getDayGan()
    de = STEM_ELEMENT[dm]
    resource = [k for k, v in GEN.items() if v == de][0]
    support_elems = {de, resource}

    gz = [ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()]
    branches = [g[1] for g in gz]
    hidden = [ec.getYearHideGan(), ec.getMonthHideGan(),
              ec.getDayHideGan(), ec.getTimeHideGan()]
    damage = branch_damage_factors(branches)

    sup = opp = 0.0
    detail = []
    for i, g in enumerate(gz):
        if i == 2:
            continue
        if STEM_ELEMENT[g[0]] in support_elems:
            sup += 10.0
            detail.append(f"stem {g[0]} +10 support")
        else:
            opp += 10.0
            detail.append(f"stem {g[0]} +10 oppose")
    for i, hs in enumerate(hidden):
        mult = (2.0 if i == 1 else 1.0) * damage[i]
        for pos, h in enumerate(hs):
            w = [10.0, 5.0, 3.0][min(pos, 2)] * mult
            if STEM_ELEMENT[h] in support_elems:
                sup += w
            else:
                opp += w
        tag = f"damage x{damage[i]:.2f}" if damage[i] < 1.0 else "undamaged"
        detail.append(f"branch {branches[i]} ({['yr', 'mo', 'dy', 'hr'][i]}) {tag}")
    state = season_state(de, branches[1])
    season_sup = {"旺": 25, "相": 15, "休": 5, "囚": 0, "死": 0}[state]
    season_opp = {"旺": 0, "相": 0, "休": 5, "囚": 10, "死": 20}[state]
    sup += season_sup
    opp += season_opp
    detail.append(f"season state {state} (+{season_sup} sup / +{season_opp} opp)")

    pct = 100.0 * sup / (sup + opp) if (sup + opp) else 50.0
    if pct >= 57:
        verdict = "身旺 STRONG"
    elif pct <= 43:
        verdict = "身弱 WEAK"
    else:
        verdict = "BORDERLINE -- give advice robust to BOTH verdicts"
    return verdict, pct, detail


def stem_combos_with_natal(stem, natal_stems):
    """Detect 五合 between an incoming stem (luck/annual) and natal stems."""
    hits = []
    for i, ns in enumerate(natal_stems):
        key = frozenset({stem, ns})
        if len(key) == 2 and key in WUHE:
            hits.append(f"{stem}{ns}合 with natal pillar {i + 1} "
                        f"(合而不化 default: binding/distraction, NOT "
                        f"transformation, while the natal stem is rooted)")
    return hits


def solar_time_correction(clock_dt, longitude, tz_meridian=120.0):
    """Approximate true solar time: longitude offset + equation of time."""
    lon_min = (longitude - tz_meridian) * 4.0
    # Equation of time, NOAA-style approximation (good to ~1 minute)
    import math
    n = clock_dt.timetuple().tm_yday
    b = 2 * math.pi * (n - 81) / 364.0
    eot = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
    return clock_dt + timedelta(minutes=lon_min + eot), lon_min, eot


def cast(dt, sect=2):
    s = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
    ec = s.getLunar().getEightChar()
    ec.setSect(sect)
    return ec


def print_chart(ec, label):
    gz = [ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()]
    day_stem = ec.getDayGan()
    names = ["Year ", "Month", "Day  ", "Hour "]
    hidden = [ec.getYearHideGan(), ec.getMonthHideGan(), ec.getDayHideGan(), ec.getTimeHideGan()]
    nayin = [ec.getYearNaYin(), ec.getMonthNaYin(), ec.getDayNaYin(), ec.getTimeNaYin()]
    print(f"=== {label} ===")
    for i, n in enumerate(names):
        stem, branch = gz[i][0], gz[i][1]
        sg = "日主" if i == 2 else ten_god(day_stem, stem)
        hid = " ".join(f"{h}:{ten_god(day_stem, h)}" for h in hidden[i])
        print(f"{n} {gz[i]}  stem={sg}  hidden[{hid}]  nayin={nayin[i]}")
    print(f"Day Master: {day_stem} ({STEM_ELEMENT[day_stem]}) | Void (空亡): {ec.getDayXunKong()}")
    inter = branch_interactions([g[1] for g in gz])
    if inter:
        print("Branch interactions:", "; ".join(inter))
    ss = shensha(gz)
    if ss:
        print("Shensha:", "; ".join(ss))
    return gz


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", required=True, help="Birth date YYYY-MM-DD (local clock)")
    ap.add_argument("--time", required=True, help="Birth time HH:MM (local clock)")
    ap.add_argument("--longitude", type=float, default=None,
                    help="Birthplace longitude in degrees E (for solar-time correction)")
    ap.add_argument("--tz-meridian", type=float, default=120.0,
                    help="Timezone standard meridian, e.g. 120 for UTC+8 (default 120)")
    ap.add_argument("--gender", choices=["male", "female"], required=True)
    ap.add_argument("--no-solar-correction", action="store_true")
    ap.add_argument("--year", type=int, default=datetime.now().year,
                    help="Year for the annual pillar (default: current year)")
    args = ap.parse_args()

    try:
        clock = datetime.strptime(f"{args.date} {args.time}", "%Y-%m-%d %H:%M")
    except ValueError as e:
        sys.exit(f"Bad date/time format: {e}")

    use_dt = clock
    if args.longitude is not None and not args.no_solar_correction:
        use_dt, lon_min, eot = solar_time_correction(clock, args.longitude, args.tz_meridian)
        print(f"Clock time {clock} -> true solar time {use_dt.strftime('%Y-%m-%d %H:%M')} "
              f"(longitude {lon_min:+.1f} min, equation of time {eot:+.1f} min)\n")

    ec = cast(use_dt)
    gz = print_chart(ec, "CHART (solar-time corrected)" if use_dt != clock else "CHART")

    verdict, pct, detail = strength_analysis(ec)
    print(f"\n=== Day Master strength (heuristic scorer) ===")
    print(f"Verdict: {verdict}  (support {pct:.0f}%)")
    for d in detail:
        print(f"  {d}")

    # If the correction changed the two-hour slot, show the clock-time variant too
    if use_dt != clock:
        ec_clock = cast(clock)
        if ec_clock.getTime() != ec.getTime() or ec_clock.getDay() != ec.getDay():
            print("\nNOTE: clock time falls in a different hour slot. Clock-time variant:")
            print_chart(ec_clock, "VARIANT (raw clock time, late-zi sect 2)")

    # Luck pillars
    yun = ec.getYun(0 if args.gender == "female" else 1)
    print(f"\n=== Luck pillars ({args.gender}, "
          f"{'forward' if yun.isForward() else 'backward'}) ===")
    print(f"First pillar begins: {yun.getStartSolar().toYmd()}")
    day_stem = ec.getDayGan()
    natal_stems = [ec.getYear()[0], ec.getMonth()[0], ec.getDay()[0], ec.getTime()[0]]
    for d in yun.getDaYun()[1:7]:
        g = d.getGanZhi()
        tg = ten_god(day_stem, g[0]) if g else ""
        combos = stem_combos_with_natal(g[0], natal_stems) if g else []
        extra = ("  [" + "; ".join(combos) + "]") if combos else ""
        print(f"  Age {d.getStartAge()}-{d.getEndAge()} ({d.getStartYear()}-{d.getEndYear()}): {g} (stem={tg}){extra}")

    # Annual pillar
    s = Solar.fromYmdHms(args.year, 6, 15, 12, 0, 0)
    annual = s.getLunar().getYearInGanZhiExact()
    combos = stem_combos_with_natal(annual[0], natal_stems)
    print(f"\nAnnual pillar {args.year}: {annual} "
          f"(stem={ten_god(day_stem, annual[0])})")
    for c in combos:
        print(f"  {c}")


if __name__ == "__main__":
    main()
