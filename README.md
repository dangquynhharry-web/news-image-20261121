# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/dangquynhharry-web/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/dangquynhharry-web/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

The World — a program that draws a newspaper front page summing up the
world's news of Saturday 21 November 2026, and writes it to
`/output/entry.png`. Entry for the make.fun bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121)
("Sum up 21 November's world news in one image").

## Run it

```sh
python3 main.py   # writes /output/entry.png (1024x1024 PNG)
```

Python 3.13, standard library only — no Pillow, no network, no clock,
no randomness: every run writes byte-identical output. The text is set
from glyph bitmaps baked from DejaVu (serif-bold for the masthead and
headlines, sans for everything else) and carried in `main.py` as base64;
the PNG itself is encoded by hand with `zlib`. The `fonts/` directory
is left in the repository unused.

## The six stories

1. **Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro'** — Fausto Isidro Meza-Flores seized in a Friday-night raid in Guasave, Sinaloa; 11 killed as gunmen fought back and torched trucks.
2. **Russian missiles land in Poland** — missiles and a jet drone breach Polish airspace as Europe holds drills nearby; NATO calls it a violation, Warsaw an intentional provocation.
3. **COP31 talks run into overtime** — nearly 200 nations deadlocked in Antalya after the draft drops all fossil-fuel language; a third draft is expected on Saturday.
4. **Trump threatens 'tremendous tax' on AI data centres built abroad** — US firms warned they risk losing America's AI lead to China if they build overseas.
5. **Houthis strike Riyadh as Saudi jets hit Yemen** — Houthis claim strikes on a Saudi power plant and port; 41 killed in Yemen airstrikes, Houthi media say.
6. **French protests shrink as cost-of-living marches go on** — 82,500 march nationwide, down from 106,000 a week earlier; 70,000 police deployed.

Plus three one-line briefs: the EU budget chief's proposed 3% digital tax, the French Senate's police shootings law, and the SpaceX Dragon cargo craft's return from the ISS.

Headlines as reported on 21 November 2026 (Reuters, AP, AFP, SCMP, Al Jazeera, via the day's news reports).

---

<sub>Entered on [make.fun](https://make.fun/?ref=n7ycm9xs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
