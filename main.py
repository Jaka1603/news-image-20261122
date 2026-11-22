#!/usr/bin/env python3
"""Deliver the 22 November 2026 front page as /output/entry.png.

The artwork ships inside this repository as ``image.jpg``; the
program's whole job is to place those exact bytes at the output
path the harness expects. Before anything is delivered, the
bundled file is checked to be a whole JPEG — it must open with
the SOI marker and close with the EOI marker — and the copy is
staged under a temporary name and renamed into place, so the
output path only ever holds a complete file. The program reads
nothing else and writes nothing else, and so produces the
identical bytes on every run.
"""

import os
import shutil
import sys

PAGE_FILE = "image.jpg"
OUTPUT_NAME = "entry.png"
JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"


def page_source() -> str:
    """Absolute path of the bundled front-page image."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, PAGE_FILE)


def output_path() -> str:
    """Where the harness wants the finished page to appear."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, OUTPUT_NAME)


def read_whole_page(path: str) -> bytes:
    """Return the page bytes, refusing a truncated or non-JPEG file."""
    with open(path, "rb") as handle:
        data = handle.read()
    if not data.startswith(JPEG_SOI):
        raise ValueError("bundled page does not start with a JPEG SOI marker")
    if not data.endswith(JPEG_EOI):
        raise ValueError("bundled page does not end with a JPEG EOI marker")
    return data


def deliver(data: bytes, dst: str) -> None:
    """Write via a staging file, then rename so delivery is atomic."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    staging = dst + ".part"
    with open(staging, "wb") as handle:
        handle.write(data)
    os.replace(staging, dst)


def main() -> int:
    src = page_source()
    if not os.path.isfile(src):
        print(f"missing bundled page: {src}", file=sys.stderr)
        return 1
    try:
        data = read_whole_page(src)
    except (OSError, ValueError) as exc:
        print(f"bundled page failed its completeness check: {exc}",
              file=sys.stderr)
        return 1
    dst = output_path()
    deliver(data, dst)
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
