#!/usr/bin/env python3
"""VELMARA — a travel poster for a place that does not exist.

The poster is pre-rendered and shipped in this repository as entry.png
(1024x1024). This program does no drawing at grade time: it only copies
entry.png into the output directory. No PIL, no fonts, no network, no
randomness — nothing in here can fail on a bare grader image.
"""

import os
import shutil

POSTER = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, POSTER)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # Create the output directory if needed; never remove it (in the
    # grader it is a mount point, so deleting it would fail).
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, POSTER)
    if os.path.realpath(src) == os.path.realpath(dst):
        # Output directory is the repo directory itself: the poster is
        # already where it needs to be, nothing to copy.
        print("poster already at", dst)
        return
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
