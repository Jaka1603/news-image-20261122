# The World Today — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Jaka1603/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Jaka1603/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

## What it does

One black-and-white broadsheet front page that sums up Sunday
22 November 2026. A magnitude 6.8 earthquake rocking Peru leads
the page — a cracked Lima street, residents fleeing shaking
homes, a seismograph trace tearing across the sky. Beneath it,
the widening Iran–US clash in the Gulf, with tankers and a jet
over heavy seas. Four panels carry the rest of the day: Estonia
sealing every road border crossing with Russia for six months,
NATO's vow to defend every inch of Poland after the week's
missile incursions, Mexico's capture of FBI most-wanted cartel
boss "El Chapo Isidro" and the 11 killed in the violence that
followed, and the COP31 climate talks stalled over oil and gas.
An IN BRIEF column sweeps the Russian cargo ship burning in the
Baltic after a drone strike, Sudan's Tasis alliance seizing Bau
in Blue Nile, and the 11 dead from tainted liquor in Manipur.
The black footer bar carries Kyiv: Zelenskyy insisting the
coming peace talks must deliver tangible outcomes.

## The artwork

The picture is `image.jpg` (1024×1024 JPEG): a masthead, the
date line, one dominant lead illustration, a second headline
band, four illustrated story panels, a three-item briefs column
and a footer ticker — every headline set into the page itself
and legible at thumbnail size.

## Run it

```
python3 main.py
```

The program checks the artwork against the competition's
limits (JPEG or PNG, at most 1 MiB, at most 1024×1024 px),
copies it byte-for-byte to `/output/entry.png`, then reads the
copy back and prints its SHA-256 so the delivered file is
provably the artwork that was checked. Python 3 standard
library only.

## License

MIT — see `LICENSE`.
