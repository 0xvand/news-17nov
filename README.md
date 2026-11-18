# The World in One Image — 17 November 2026

An entry for make.fun's **news-image-20261117** bounty: sum up the world
news of Tuesday 17 November 2026 in one image.

`entry.png` is a newspaper front page for the day — a lead story on the
U.S. strikes on Iran's Qeshm Island and the burning tankers in the Strait
of Hormuz, plus panels on the Kerch Bridge strike, the Shenzhen APEC
summit, Gaza aid, the COP31 draft deal, U.S. AI chip rules, the U.S.
losing measles elimination status, and a markets ticker.

- `main.ts` — the entry program (Node 22, standard library only). It
  copies `entry.png` to `/output/entry.png`, byte for byte, every run.
- `make_image.py` — the Pillow script that drew `entry.png` from the
  day's headlines, using real fonts so every word is crisp.
- `SOURCES.md` — the reporting behind every headline on the page, with
  the stories cross-checked and one popular story deliberately left off
  because it happened on a different day.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Licensed under the MIT License (see `LICENSE`).
