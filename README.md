# Chinese Metaphysics Skill for Claude Code

A deterministic, reference-backed skill for casting and interpreting
classical Chinese metaphysics charts: **BaZi** (四柱八字 — Four Pillars of Destiny),
**Zi Wei Dou Shu** (紫微斗数 — Purple Star Astrology), and **Qi Men Dun Jia**
(奇门遁甲 — Mysterious gates Divination).

All calculations run through verified Python scripts with documented
methodology so you understand why interpretations differ between
schools and practitioners.

## Why this skill

- **Deterministic calculations** — no mental math, no silent failures
  at solar-term boundaries
- **School differences documented** — understand why practitioners
  disagree (solar time correction, strength scoring, Life lord convention)
- **Verification built in** — validate charts from other apps against
  our engine
- **Production ready** — 16 regression tests ensure accuracy across
  updates

## What you can do

- **Cast BaZi charts** — Four Pillars with luck pillars and annual overlays
- **Generate Zi Wei Dou Shu readings** — Purple Star charts with decade
  and annual forecasts
- **Perform Qi Men divination** — determine auspicious timing for decisions
- **Check compatibility** — cross-examine multiple natal branches
- **Verify external charts** — reproduce charts from other practitioners
  and apps to compare methodology

## Installation

```bash
npx -y skills add chloechewx/chinese-metaphysics-skill \
  --skill chinese-metaphysics
```

## Requirements

- **Python 3.10+** (installed on your system)
- Dependencies auto-install on first use:
  - `lunar-python`, `py-iztro` (BaZi + Zi Wei calculations)
  - `kinqimen`, `ephem` (Qi Men divination)

## Quick start

Ask Claude to cast a chart with a birth date, time, location, and gender:
```
Cast my BaZi: born 1990-05-15, 14:30, Singapore, female
```

Other common requests:
- "Give me a Zi Wei reading for the same chart"
- "Is this a good time to start a new project?" (Qi Men timing)
- "Check compatibility: my chart vs someone born 1988-03-22"
- "I have a chart from [insert Screenshot] — does it match yours?"

## Testing

```bash
python scripts/run_tests.py
```

16 assertions against a verified gold chart. Run after any environment
change or library upgrade.

## Feedback & contributions

Found a calculation error, a methodology fork that isn't documented,
or a chart that doesn't match your expectations?

- **GitHub Issues** — open an issue at
  `https://github.com/chloechewx/chinese-metaphysics-skill/issues`
- **Email** — invertedspearofheaven@proton.me


## License

MIT