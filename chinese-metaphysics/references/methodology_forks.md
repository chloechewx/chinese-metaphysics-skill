# Methodology forks: where legitimate readings diverge

These are points where different classical schools make different choices.
None is a calculation error. When a chart from another source disagrees with
ours, check this list FIRST before assuming a bug. Always disclose the
relevant fork to the user when it materially changes the reading.

## 1. True solar time vs clock time (affects all three systems)

Clock time uses the timezone meridian (120E for UTC+8); the sun does not.
Correction = (longitude - meridian) x 4 minutes + equation of time.
Example: Singapore (103.85E) clock runs ~65 min ahead of solar time, so a
23:20 birth is ~22:19 solar -- Hai hour, not Zi hour. Engines split by
school: some professional engines use TRUE SOLAR TIME; other engines
following the clock-time school (verified empirically
2026-06: gold chart yields hour 甲子 there vs 癸亥 here) use CLOCK TIME
with no longitude correction. Neither is a bug. Our scripts default to
solar time when --longitude is given; pass --no-solar-correction to
reproduce clock-time-school charts. ALWAYS report when the correction
changes the two-hour slot, and show both variants.

## 2. Late Zi hour (23:00-23:59) day boundary (BaZi)

School A (sect 1): the day advances at 23:00. School B (sect 2): the day
advances at midnight; 23:00-23:59 uses the next day's Zi-hour stem but
today's day pillar. lunar-python supports both via setSect(). Default:
sect 2. Only matters when, after solar correction, the time still falls
in 23:00-23:59.

## 3. Day Master strength scoring (BaZi) -- THE BIG ONE

The verdict (身旺 strong vs 身弱 weak) flips the favorable elements and
therefore most of the practical advice. The naive method counts three
checks -- 得令 (in season), 得地 (rooted in branches), 得势 (supported by
stems) -- and calls 2/3 strong. More sophisticated engines apply damage
modifiers: a root that is clashed (冲) or self-punished (自刑) is
discounted, sometimes heavily, which can flip a naive "strong" to "weak".
Documented live example: chart 庚辰/辛巳/癸亥/癸亥 scores strong on naive
count (fails only 得令) but a damage-modifier engine scored it weak
because both 亥 roots are clashed by 巳 and self-punish each other.
Protocol: state the verdict you computed, state which method you used,
flag if the chart is near the boundary, and present advice that survives
both verdicts where possible.

## 4. Useful god (用神) selection (BaZi)

Strength-based school: strong DM favors draining/controlling elements,
weak DM favors resource/peer elements. Climate school (穷通宝鉴): each
day-stem x month-branch cell prescribes preferred stems regardless of
strength. Engines blend these differently. Disclose which logic you used.

## 5. Life lord 命主 convention (Zi Wei)

School A derives it from the Life palace branch (py-iztro does this).
School B derives it from the birth-year branch.
Same chart can show 破军 under A and 廉贞 under B. cast_ziwei.py prints
both. Body lord 身主 is consistent across schools.

## 6. Qi Men plate arrangement and ju selection

转盘 (rotating plate) vs 飞盘 (flying palace) schools arrange the chart
differently; 拆补 vs 置闰 select the ju differently near solar-term
boundaries. kinqimen's pan(1) = 拆补, pan(2) = 置闰, rotating-plate style.
Charts from other apps may differ for these reasons.

## 7. Combination transformation (合化 vs 合而不化) (BaZi)

A stem combination (e.g. 戊癸合) only transforms (化火) if the resulting
element is supported by season and the combined stem is not strongly
rooted. A day master with strong roots essentially never transforms --
read it as 合而不化 (binding/distraction), not transformation. Overclaiming
transformation is a common error in AI-generated readings.
