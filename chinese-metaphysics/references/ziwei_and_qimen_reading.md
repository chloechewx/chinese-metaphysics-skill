# Zi Wei Dou Shu reading workflow

Run scripts/cast_ziwei.py first. Interpret only from its output.

## The 14 main stars, one-line cores

紫微 Emperor: dignity, leadership, needs capable support
天机 Strategist: agile mind, planning, restlessness
太阳 Sun: visibility, giving, masculine/father figures, career shine
武曲 General: finance, decisiveness, metal-hard execution
天同 Child: ease, enjoyment, blessings, low aggression
廉贞 Politician: intensity, desire, principled or transgressive
天府 Treasurer: stability, conservation, stewardship
太阴 Moon: feminine/mother figures, property, quiet wealth, emotion
贪狼 Wolf: desire, versatility, social magnetism, indulgence risk
巨门 Giant Gate: speech, debate, scrutiny; words as weapon both ways
天相 Chancellor: service, image, mediation
天梁 Elder: protection, principles, surviving trouble then helping others
七杀 Marshal: courage, upheaval, all-in execution
破军 Vanguard: breaking and rebuilding, pioneering, volatility

## Reading procedure

1. Life palace (命宫) star + brightness = core temperament. Empty palace
   borrows from the opposite palace (迁移).
2. Body palace (身宫) = where life's center of gravity shifts after ~35,
   and the domain fused with self-image. Body palace in Spouse palace =
   relationships are constitutive of identity, for example.
3. Four transformations (四化) by birth-year stem: 化禄 (flow/gain),
   化权 (power/control), 化科 (reputation/refinement), 化忌 (obstruction/
   attachment -- the knot of the chart). The palace holding 化忌 is where
   the user ruminates; name it carefully and constructively.
4. Triangle (三方四正): a palace is read with its trine palaces and
   opposite. Career = Life + Career + Wealth + Travel as a system.
5. Decades (大限): the active decade palace becomes a second Life palace
   overlaying the natal chart. Note which natal stars and transformations
   it activates. Annual (流年) overlays likewise for year questions.
6. Decade flying transformations (大限四化): each decade palace carries a
   heavenly stem (printed by cast_ziwei.py); that stem fires its own four
   transformations onto the natal stars. Where the decade's 禄 lands shows
   the decade's gains; where its 忌 lands shows the decade's knot. A decade
   忌 landing on a natal 化忌 star doubles that theme for the decade.
7. Self-transformation (自化): when a palace's own stem fires a
   transformation onto a star sitting IN that palace (e.g. 戊 palace stem
   with 天机 inside -> 天机自化忌). School-dependent technique (飞星派 /
   钦天四化); use it as supporting color, not as a primary verdict, and
   say it is school-specific if asked.

## Alternate palace meanings (use when the question fits)

父母宫 doubles as the documents/contracts palace (文书宫) -- read it for
legal matters, paperwork, certifications. 疾厄宫 doubles as the workplace
interior. 仆役/交友宫 covers business partners and clients, not only
friends. 田宅宫 covers office premises and asset base for business
questions.

## Relationship timing technique (cross-system)

For "when/where will I meet a partner": (a) locate the spouse star in
BaZi (正官 for yin-stem females, 正财 for males etc.) -- its palace = the
meeting channel (month pillar = work/career environment, etc.); (b) check
红鸾/天喜 palace placement for the social channel; (c) candidate years are
those whose annual stem makes the spouse star transparent (e.g. 戊 years
for a 癸 female) or whose branch combines into the spouse palace; (d) check
whether the current Zi Wei decade sits on or flies 禄/科 into the spouse
palace. Converging signals across (a)-(d) justify naming a window; a
single signal does not justify naming a specific year with confidence.

## Cross-checking with BaZi

When both charts are cast for the same person, look for corroboration
(e.g. 巨门 Life palace and a BaZi 伤官 structure both indicating sharp
speech) and present convergent findings with more weight. Divergences are
fine -- the systems measure differently; say so.

---

# Qi Men Dun Jia reading workflow

Run scripts/cast_qimen.py for the moment the QUESTION is asked (时家奇门),
not the user's birth time. Qi Men is a decision/timing oracle, not a natal
system.

## Components per palace

- Deity (神): 值符 authority/protection, 螣蛇 entanglement, 太阴 hidden
  help, 六合 cooperation, 勾陈/白虎 conflict, 朱雀 documents/talk,
  九地 stability/defense, 九天 expansion/boldness
- Star (星): 天心 leadership/medicine, 天任 steadiness, 天辅 culture/exams,
  天禽 balance, 天英 brilliance/volatility, 天蓬 risk/water, 天冲 action,
  天柱 destruction/speech, 天芮 illness/learning
- Gate (门): 开 opening (favorable), 休 rest (favorable), 生 vitality
  (favorable), 伤 injury, 杜 blockage, 景 display/documents, 死 stagnation,
  惊 alarm/disputes
- Stems: 乙丙丁 the three nobles (奇), 戊 capital, 己 pitfalls, 庚 obstacle/
  opponent, 辛 fault, 壬 entanglement, 癸 conclusion

## Basic procedure

1. Identify the 用神 (focus) for the question type: self = day stem palace
   or 值符; the matter's counterpart = hour stem palace; money = 生门;
   career = 开门; relationship = 六合; documents/exams = 景门 or 天辅.
2. Locate the focus palace; read deity + star + gate + stem combination
   and the palace's five-element relationship to the focus.
3. Favorable gates landing in palaces that support the asker's day stem =
   green light; 庚 sitting on the focus = obstruction; check 空亡 (void)
   palaces -- matters there are hollow or delayed.
4. Answer the specific question asked with a clear lean plus the main
   caveat. Qi Men answers should be short and concrete.

## Guardrails

Same honesty rules as BaZi. Additionally: never cast Qi Men charts to
advise on medical decisions, legal matters, or gambling-style financial
bets; redirect to the real-world basis of those decisions.
