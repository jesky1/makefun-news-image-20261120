[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/jesky1/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/jesky1/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — Friday 20 November 2026

A single-page newspaper front page that compresses one day of world news —
Friday 20 November 2026 — into one 1024×1024 image. The photograph of the
Peace Palace in The Hague (`hero.webp`) is text-free; every word on the page
is typeset programmatically by `compose.py` (Python 3 + Pillow), so the page
is fully deterministic: run the script twice and you get a byte-identical
`entry.png`.

## What is on the page

- **The Hague (lead story)** — The International Court of Justice ruled 9–6
  that Myanmar's military committed genocide against the Rohingya minority in
  northern Rakhine State, the first time the court has held a state
  responsible for genocide. The hero photograph shows the Peace Palace at
  dawn, flags flying, as crowds gathered for the judgment.
- **Kyiv** — Overnight Russian missile and drone strikes hit bridges across
  the Dnipro River, killing eight people and wounding 28 across nine regions;
  Poland reported its airspace violated and Estonia announced a six-month
  border closure with Russia.
- **Shenzhen** — Presidents Trump, Xi and Putin issued a four-point joint
  declaration after their first trilateral meeting, but 70 minutes of talks
  produced no breakthrough on Ukraine, Iran or nuclear weapons; in Berlin,
  envoy Jared Kushner said Russia was "comfortable" with NATO Article 5-style
  security guarantees for Ukraine.
- **Riyadh** — A Houthi missile struck Riyadh's financial district and
  damaged the Public Investment Fund tower; Saudi Arabia intercepted another
  missile and five drones.
- **Markets** — Anthropic closed 17% above its offer price on its Nasdaq
  debut, while the S&P 500 fell for a fifth straight day, the Nikkei dropped
  4.8%, SoftBank plunged 16% and gold fell 4.2%; the IMF warned global public
  debt is nearing 100% of world GDP.
- **Also today** — GTA VI's record $2.36 billion first-day launch; Kenya
  discharges its last Ebola patient; Ukraine hits the Kerch Bridge again; the
  US Senate blocks a bid to end the Iran war 51–48; youth cost-of-living
  protests in more than 25 countries; the IAEA says North Korea is expanding
  uranium enrichment.

Sources: compiled from news reporting of Friday 20 November 2026 — wire
services and international outlets.

## Running it

The runner (`main.ts`, Node standard library only) copies `entry.png` into
the output directory and verifies the copy is a non-empty PNG of at most
1 MiB:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To rebuild the page itself from the photograph and the typesetting script:

```sh
python3 compose.py
```

## License

MIT — see `LICENSE`.
