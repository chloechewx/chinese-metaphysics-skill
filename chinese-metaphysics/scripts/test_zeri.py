#!/usr/bin/env python3
"""Regression tests for cast_zeri.py. Run: python test_zeri.py (exit 0 = pass)

Gold values cross-verified against tyme4ts@1.2.2 (independent implementation,
same almanac tradition) on 2026-07-24: day pillar, 建除, 二十八宿, 十二天神,
and the full 宜/忌 lists matched for 2026-07-28 and 2026-08-03.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "cast_zeri.py")
FAILURES = []


def run(args):
    r = subprocess.run([sys.executable, SCRIPT] + args,
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout


def check(label, cond, detail=""):
    if not cond:
        FAILURES.append(f"{label}{': ' + str(detail) if detail else ''}")


def day(args):
    code, out = run(args + ["--json"])
    check("script ran " + args[1], code == 0, out[:200])
    return json.loads(out)["days"][0] if code == 0 else {}

d = day(["--start", "2026-08-03", "--activity", "开市"])
check("gold pillar 己酉", d.get("pillar") == "己酉", d.get("pillar"))
check("gold duty 满", d.get("duty") == "满", d.get("duty"))
check("gold star28 危", d.get("star28") == "危", d.get("star28"))
check("gold tianshen 勾陈", d.get("tianshen") == "勾陈", d.get("tianshen"))
check("gold 开市 in 宜", d.get("activity") == "宜 YES", d.get("activity"))

d = day(["--start", "2026-07-28", "--activity", "开市"])
check("0728 pillar 癸卯", d.get("pillar") == "癸卯", d.get("pillar"))
check("0728 duty 成", d.get("duty") == "成", d.get("duty"))
check("0728 star28 尾", d.get("star28") == "尾", d.get("star28"))
check("0728 开市 in 忌", d.get("activity") == "忌 AVOID", d.get("activity"))

d = day(["--start", "2026-07-30", "--natal", "亥,亥"])
check("巳 clashes 亥 x2", "x2" in " ".join(d.get("natal", [])),
      d.get("natal"))
d = day(["--start", "2026-08-02", "--natal", "亥,亥"])
check("申 harms 亥 x2", "害" in " ".join(d.get("natal", [])), d.get("natal"))
d = day(["--start", "2026-07-29", "--natal", "辰"])
check("辰 self-punish", "自刑" in " ".join(d.get("natal", [])), d.get("natal"))
d = day(["--start", "2026-07-25", "--void", "子,丑"])
check("子 void flagged", "空亡" in " ".join(d.get("natal", [])), d.get("natal"))
d = day(["--start", "2026-07-31", "--natal", "亥,亥,辰,巳"])
check("clean day has no natal flags", d.get("natal") == [], d.get("natal"))

code, out = run(["--start", "2026-08-03", "--hours", "--activity", "开市",
                 "--natal", "亥,亥,辰,巳", "--json"])
h = json.loads(out)["days"][0].get("hours", []) if code == 0 else []
check("12 hours returned", len(h) == 12, len(h))
check("hour natal clash flagged",
      any("冲" in x.get("natal", "") for x in h),
      [x.get("natal") for x in h])

check("bad date rejected", run(["--start", "2026-13-45"])[0] == 2)
check("bad branch rejected",
      run(["--start", "2026-08-03", "--natal", "XX"])[0] == 2)
check("reversed range rejected",
      run(["--start", "2026-08-03", "--end", "2026-07-01"])[0] == 2)
check("hours+range rejected",
      run(["--start", "2026-08-01", "--end", "2026-08-03", "--hours"])[0] == 2)
check("out-of-range year rejected", run(["--start", "1850-01-01"])[0] == 2)

if FAILURES:
    sys.stderr.write("FAIL:\n  " + "\n  ".join(FAILURES) + "\n")
    sys.exit(1)
print("All zeri tests passed.")
