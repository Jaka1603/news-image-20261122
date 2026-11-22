#!/usr/bin/env python3
"""Deliver the day's front page to the grader, unchanged.

The artwork for this entry lives next to this script as image.jpg.
This program is its courier and its inspector in one: it confirms
the file is a complete JPEG or PNG inside the competition's size
limits, copies it byte for byte to the output folder as entry.png,
then reads the copy back and compares fingerprints so a truncated
or corrupted copy can never be mistaken for the real page.
Only the Python standard library is used.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576  # 1 MiB, the competition's file-size ceiling
MAX_SIDE = 1024        # no side of the picture may exceed this

JPEG_SOI = b"\xff\xd8"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# JPEG markers that carry no length field and no payload.
STANDALONE = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))
# Start-of-frame markers; their segment holds the picture's size.
FRAME_MARKERS = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
}


def die(message):
    print("entry error: " + message, file=sys.stderr)
    sys.exit(1)


def png_dimensions(blob):
    """Width and height sit at fixed offsets inside the IHDR chunk."""
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        die("PNG is missing its IHDR chunk")
    width = struct.unpack_from(">I", blob, 16)[0]
    height = struct.unpack_from(">I", blob, 20)[0]
    return width, height


def jpeg_dimensions(blob):
    """Walk the segment chain until a start-of-frame marker appears."""
    cursor = 2  # the SOI marker occupies the first two bytes
    while cursor + 3 < len(blob):
        if blob[cursor] != 0xFF:
            die("JPEG segment chain is broken at byte %d" % cursor)
        marker = blob[cursor + 1]
        if marker == 0xFF:
            cursor += 1  # padding byte before the real marker
            continue
        if marker in FRAME_MARKERS:
            height = struct.unpack_from(">H", blob, cursor + 5)[0]
            width = struct.unpack_from(">H", blob, cursor + 7)[0]
            return width, height
        if marker in STANDALONE:
            cursor += 2
            continue
        segment_length = struct.unpack_from(">H", blob, cursor + 2)[0]
        if segment_length < 2:
            die("JPEG segment claims an impossible length")
        cursor += 2 + segment_length
    die("no start-of-frame marker found in this JPEG")


def load_and_check(path):
    if not os.path.isfile(path):
        die("artwork not found: " + path)
    size_on_disk = os.path.getsize(path)
    if size_on_disk == 0:
        die("artwork is an empty file")
    if size_on_disk > MAX_BYTES:
        die("artwork is %d bytes; the limit is %d" % (size_on_disk, MAX_BYTES))
    with open(path, "rb") as handle:
        blob = handle.read()
    if len(blob) != size_on_disk:
        die("artwork changed size while it was being read")
    if blob[:8] == PNG_SIGNATURE:
        kind = "PNG"
        width, height = png_dimensions(blob)
    elif blob[:2] == JPEG_SOI:
        kind = "JPEG"
        width, height = jpeg_dimensions(blob)
    else:
        die("first bytes match neither JPEG nor PNG")
    if not (1 <= width <= MAX_SIDE and 1 <= height <= MAX_SIDE):
        die("picture is %dx%d; each side must be within 1..%d"
            % (width, height, MAX_SIDE))
    return blob, kind, width, height


def deliver(blob):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).digest() != hashlib.sha256(blob).digest():
        die("the delivered copy differs from the artwork")
    return target


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    blob, kind, width, height = load_and_check(os.path.join(here, "image.jpg"))
    target = deliver(blob)
    print("%s %dx%d, %d bytes, sha256 %s -> %s"
          % (kind, width, height, len(blob),
             hashlib.sha256(blob).hexdigest(), target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
