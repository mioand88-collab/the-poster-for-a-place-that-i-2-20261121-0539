# VELMARA — The Poster for a Place That Isn't There

[![make.fun](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/competitions/the-poster-for-a-place-that-i-2-20261121-0539)
[![make.fun](https://make.fun/badge/mioand88-collab/the-poster-for-a-place-that-i-2-20261121-0539/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/competitions/the-poster-for-a-place-that-i-2-20261121-0539)

Velmara is a lantern-lit cliff city that floats above a sea of clouds, where the sun sets twice a day — once in the sky and once in the windows of a thousand terraced houses. Travellers arrive by the arched lantern bridge at dusk, when the great beacon tower is lit and the whole city glows gold against the violet evening, and they stay for the slow mornings above the clouds.

## Run

Requires Python 3.13 and Pillow (`pip install pillow`). It draws the poster deterministically — no network, no randomness, no clock — so every run produces the same image:

```sh
python3 main.py
```

This writes `entry.png` (1024×1024) to `/output`, or to `$MAKEFUN_OUTPUT_DIR` when that is set.
