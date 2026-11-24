#!/usr/bin/env python3
"""Copy-only entrypoint for the 23 November 2026 news poster.

Reads the pre-generated entry.png sitting beside this file and
copies it, byte for byte, to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). Standard library only, no network, deterministic.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    # sanity: the copy must be byte-identical to the source
    if os.path.getsize(SOURCE) != os.path.getsize(dest):
        print("copy size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
