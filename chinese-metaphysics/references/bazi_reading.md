# BaZi reading workflow

Run scripts/cast_bazi.py first. Interpret only from its output -- never
recompute pillars, shensha, or luck pillars from memory.

**Read the chart in isolation.** Base the reading only on the chart output in
front of you. Do not pull in anything you happen to know about this person from
elsewhere (their job, studies, travel, past chats, or other notes) -- it
contaminates the reading. The chart speaks for itself.

## Ten gods: core meanings (relative to the Day Master)

- 比肩 Friend: peers, independence, self-reliance, competition
- 劫财 Rob Wealth: rivals, wealth contested by peers, charisma, risk-taking
- 食神 Eating God: gentle output, enjoyment, nurturing creativity
- 伤官 Hurting Officer: sharp output, technical/creative skill, eloquence,
  rebellion against authority
- 正财 Direct Wealth: earned income, stability, frugality; (trad.) wife star
  in male charts
- 偏财 Indirect Wealth: windfalls, business income, generosity; father star
- 正官 Direct Officer: structure, employment, discipline, reputation;
  (trad.) husband star in female charts
- 七杀 Seven Killings: pressure, drive, authority taken by force, crisis
- 正印 Direct Resource: learning, credentials, protection, mother star
- 偏印 Indirect Resource: unconventional learning, intuition, solitude

Read the chart's dominant gods as the personality skeleton; read what is
WEAK or ATTACKED as the life-area requiring management (e.g. weak clashed
wealth star = money retention is the issue, not earning).

## Strength analysis procedure

Use the scorer built into cast_bazi.py -- do NOT hand-count. It applies
season state (旺相休囚死), root weights with clash/punishment/harm damage
multipliers, and stem support, then reports a percentage and verdict with
an explicit BORDERLINE band (43-57%).

- STRONG verdict: output/wealth/officer elements favorable.
- WEAK verdict: resource/peer elements favorable (officer only via the
  官印相生 bridge when resource is strong -- state that conditionality).
- BORDERLINE: do not pick a side silently. Present advice that survives
  both verdicts, name the fork, and offer the lived-experience calibration
  test: identify past years that were favorable under one verdict and
  unfavorable under the other, and ask which matched. Adjudicated example:
  庚辰/辛巳/癸亥/癸亥 scores 55% borderline -- a naive count says strong, a
  damage-weighted engine said weak; both are defensible, which is exactly
  what the borderline band encodes.

The script also auto-detects 五合 stem combinations between luck/annual
stems and natal stems, defaulting to 合而不化 (binding, not transformation)
while the natal stem is rooted. Never claim a combination "turns" the Day
Master into another element when the DM has roots -- this is a documented
recurring error in AI-generated readings.

## Interactions to weight heavily

- Clash (冲) on the month pillar = unstable career environment
- Self-punishment (自刑) on day/hour = self-generated friction, overthinking
- Combinations (合) binding the useful god = support tied up
- Day-pillar special flags (阴差阳错, 十恶大败) = relationship-communication
  and effort-reward cautions respectively; frame as management advice, not doom

## Luck pillars and annual pillars

The decade (大运) sets the backdrop; the year (流年) triggers events. For
each, derive the stem's ten god and check the branch's interactions with
the natal branches. A year whose branch adds a third instance of an
existing clash amplifies it. Past years that activated chart features are
useful calibration questions for the user ("did 20XX feel like...").

## Compatibility questions (partner / friends / colleagues)

ALWAYS run scripts/check_compat.py rather than reasoning from one anchor
branch -- single-anchor reasoning is the documented source of errors
(e.g. ranking a sign ideal via the day branch while missing its clash
with the year branch, or recommending a void branch without caveat).

Rules:
- Anchor conventions: day branch governs romance (spouse palace), year
  branch governs friendships/social, element gaps (not zodiac) govern
  work relationships. But every candidate must still be checked against
  ALL FOUR natal branches plus the void pair -- mixed results are
  presented as "strong, with a named cost", never silently simplified.
- Romance timing/profile bonus: candidate birth YEARS whose stem is the
  natal spouse star (e.g. 戊 years for a 癸 female) stack with branch
  compatibility (e.g. 戊寅 for a chart whose spouse palace combines 寅).
- Ages must be DERIVED from compatible zodiac years (12-year cycle), not
  invented as ranges. Sanity-check any age range against the caution
  list: a range that includes excluded zodiac years is self-contradictory.
- Void (空亡) branches get an explicit caveat: connections classically
  read as hollow, delayed, or hard to solidify.
- Close with the standing honesty note: year-branch matching uses one of
  a person's eight characters; real people beat tables.

## Output structure

Write the reading in this order, using these exact section headings so every
reading looks the same. Lead each section with the plain-English point, then
name the technical reason in parentheses. Keep each section tight -- a few
sentences, not a wall of text.

### The short version
One or two sentences: what kind of chart this is and the single feature that
shapes everything else. The reader should get the gist here before any detail.

### Your core nature
The day pillar's basic temperament plus the one or two strongest ten gods,
described as character traits in everyday language. Fold in standout stars
(e.g. 华盖 artistic solitude, 孤辰 emotional self-sufficiency) only if present.

### What you've got going for you
Dominant gods and helpful (noble) stars, framed as real strengths the reader
can lean on.

### What to keep an eye on
Weak or attacked gods and punishment flags, framed as areas to manage -- never
as flaws or fate. Say what the issue actually looks like in daily life
(e.g. "money tends to leak out faster than it comes in").

### Work and money
Which gods support which kinds of work, and how steady the career backdrop is
(month-pillar stability). Translate into concrete work styles, not labels.

### Timing
Only when the reader asks about timing. Cover the current decade's flavour, any
specific year they named, and better windows ahead (include favourable months
if they asked about a particular year). Frame as "seasons that suit X", not
"good year / bad year".

### People to be mindful of
Only when relevant. Who or what to handle with care, drawn from 劫财 / 劫煞 /
亡神 and the chart's weak spots. Keep it about dynamics to watch, not warnings.

End with one line reminding the reader this is a lens for reflection, not a
forecast.

## Tone and honesty guardrails

- This is a classical framework for self-reflection, not a prediction engine.
  Present the reading as a mirror, not a forecast.
- Never turn timing into instructions for big decisions (starting a business,
  marriage, anything medical). Always point back to real-world factors.
- Don't invent stars (shensha) or interactions that aren't in the script output.
- Explain every Chinese term the first time you use it, in plain words.
- Write "negative" flags as things to manage, not things to fear.
- Keep the language natural and direct. Skip the mystical register -- say what
  a feature means for the reader's actual life.
