[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/tachyon0215/muse-news-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/tachyon0215/muse-news-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# The World in One Image — Tuesday 17 November 2026

An entry for the make.fun competition
[news-image-20261117](https://make.fun/c/news-image-20261117):
sum up the world news of Tuesday 17 November 2026 in a single image.

`main.ts` (Node 22, standard library only) copies the bundled `entry.png`
(1024×1024) to `/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR/entry.png`
outside the grader. The image is drawn by `draw.py` (Pillow) from the five
stories researched in `NOTES.md`:

- Bridges hit in the Ukraine war (Kyiv bridges struck; Crimea bridge damaged)
- Quad leaders meet in Manila (first summit since 2024)
- Iran drones target a US radar site in Bahrain (intercepted)
- Nvidia sales double again ($115.8B revenue on AI demand)
- Red crabs march to the sea on Christmas Island

## Run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
