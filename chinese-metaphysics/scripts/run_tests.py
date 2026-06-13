#!/usr/bin/env python3
"""Verify the casting scripts against known, externally-verified charts.

Gold chart: 2000-05-05 23:20 Singapore (lon 103.85E, UTC+8), female.
Verified against an independent professional engine
on 2026-06-12: pillars, hidden stems, ten gods, nayin, interactions,
and the full 12-palace Zi Wei chart all matched.

Run: python run_tests.py   (from the scripts/ directory)
Exit code 0 = all pass.
"""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FAILURES = []


def run(script, args):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)] + args,
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        FAILURES.append(f"{script} exited {r.returncode}: {r.stderr.strip()[:300]}")
        return ""
    return r.stdout


def check(label, output, *needles):
    missing = [n for n in needles if n not in output]
    if missing:
        FAILURES.append(f"{label}: missing {missing}")
        print(f"  FAIL {label}: missing {missing}")
    else:
        print(f"  PASS {label}")


print("== BaZi: gold chart (solar-time corrected -> Hai hour) ==")
out = run("cast_bazi.py", ["--date", "2000-05-05", "--time", "23:20",
                           "--longitude", "103.85", "--gender", "female",
                           "--year", "2026"])
check("pillars", out, "庚辰", "辛巳", "癸亥")
check("hour pillar is 癸亥 not 甲子", out, "Hour  癸亥")
check("clock-time variant reported", out, "VARIANT", "甲子")
check("ten gods", out, "正印", "偏印", "比肩", "劫财", "伤官")
check("interactions", out, "巳亥冲", "亥亥自刑")
check("shensha", out, "月德", "华盖", "孤辰", "亡神", "阴差阳错", "十恶大败")
check("luck pillars backward female", out, "戊寅", "丁丑")
check("2026 annual pillar", out, "丙午")
check("strength scorer borderline on gold chart", out, "BORDERLINE", "support 55%")
check("season state computed", out, "season state 囚")
check("damage modifiers applied", out, "damage x0.25", "damage x0.30")
check("wuhe combos detected with anti-overclaim note", out, "戊癸合", "丙辛合", "合而不化")

print("== BaZi: no-correction control (late zi, day kept) ==")
out = run("cast_bazi.py", ["--date", "2000-05-05", "--time", "23:20",
                           "--gender", "female", "--no-solar-correction"])
check("hour pillar is 甲子", out, "Hour  甲子")

print("== BaZi: strong-chart control (metal DM in metal season) ==")
out = run("cast_bazi.py", ["--date", "1995-08-17", "--time", "08:30",
                           "--longitude", "121.5", "--gender", "male"])
check("clearly strong chart scores STRONG", out, "身旺 STRONG")

print("== Zi Wei: gold chart ==")
out = run("cast_ziwei.py", ["--date", "2000-05-05", "--time", "23:20",
                            "--longitude", "103.85", "--gender", "female"])
check("bureau", out, "木三局")
check("life palace ju men at wu", out, "巨门")
check("four transformations of geng year", out, "太阳化禄", "武曲化权", "太阴化科", "天同化忌")
check("body lord", out, "文昌")
check("both life-lord schools shown", out, "破军", "廉贞")
check("palace stems and decade sihua", out, "庚辰", "大限四化", "禄:太阳@官禄")

print("== Compatibility checker: gold chart ==")
out = run("check_compat.py", ["--natal", "辰", "巳", "亥", "亥",
                              "--void", "子丑", "--all"])
check("rooster top with year six-combo", out, "酉 Rooster", "六合@year")
check("void branches flagged", out, "VOID")
check("tiger mixed profile caught", out, "害@month")
check("pig self-punishment caught", out, "自刑@day")

print("== Qi Men: smoke test ==")
out = run("cast_qimen.py", ["--datetime", "2026-06-12 10:20",
                            "--longitude", "103.85"])
check("structure", out, "陽遁三局", "值符", "值使", "旬空")
check("nine palaces rendered", out, "巽(SE)", "坎(N)", "中宫")

print()
if FAILURES:
    print(f"{len(FAILURES)} FAILURE(S):")
    for f in FAILURES:
        print(" -", f)
    sys.exit(1)
print("All tests passed.")
