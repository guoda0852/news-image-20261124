# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/guoda0852/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/guoda0852/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world news of Tuesday 24 November 2026: a newspaper-style infographic (1024x1024 PNG) drawn in pure Python, with six verified stories — the FIDE world chess title match opener in Geneva, a M5.6 earthquake in Nepal, a Politburo probe in China, a Riyadh tower attack, a Trump–Rutte meeting, and 175 migrants unaccounted for off Senegal.

## Run it

```sh
python3 main.py
```

Writes `output/entry.png` (1024x1024, about 22 KB). Python 3.13, standard library only, no network. Two runs produce byte-identical output.

## Files

- `main.py` — the program: a 5x7 bitmap font, canvas primitives, six story blocks and a PNG encoder, all in one file.
- `NOTES.md` — the six stories, their dates and primary sources, and what was deliberately left out.
- `output/entry.png` — the generated image (regenerated on every run).

## Verification

Every story was checked against reporting dated 24 November 2026 (ChessBase, Reuters, Xinhua). Aggregator "24 Nov headlines" pages recycle 21–23 Nov stories; those were excluded, as was the Ma death-sentence case (first published 23 Nov, and Reuters could not independently verify it). See `NOTES.md` for the full list.

---

<sub>Entered on [make.fun](https://make.fun/?ref=gftsjz4e&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
