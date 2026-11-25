#!/usr/bin/env python3
"""The Most Shameless Lie (u-danu-the-most-shameless-lie-fbb85bc6).

Writes one five-word confession to /output/entry.txt. The lie is the
whole entry: the confession up front, the shameless second turn in the
final word. Nothing else is written — no newline, no padding — and the
bytes on disk are read back and checked before the program reports
success.
"""

import os
import sys

LINE = "I texted your ex. Twice."
FILE = "entry.txt"


def gate_ok(text):
    """Kit gate: 1-88 chars, 1-5 words, single clean line."""
    if text != text.strip() or not text:
        return False
    if len(text) > 88 or not 1 <= len(text.split()) <= 5:
        return False
    return "\n" not in text and "\r" not in text and all(ord(c) > 31 for c in text)


def find_out():
    """First writable candidate wins: the grader's /output, else ./out."""
    here = os.path.dirname(os.path.abspath(__file__))
    for folder in ("/output", os.path.join(here, "out")):
        try:
            os.makedirs(folder, exist_ok=True)
            test = os.path.join(folder, ".probe")
            with open(test, "wb"):
                pass
            os.remove(test)
            return folder
        except OSError:
            pass
    return None


def main():
    if not gate_ok(LINE):
        sys.exit("gate failed for entry")
    folder = find_out()
    if folder is None:
        sys.exit("no writable output directory")
    payload = LINE.encode("utf-8")
    path = os.path.join(folder, FILE)
    with open(path, "wb") as handle:
        handle.write(payload)
    with open(path, "rb") as handle:
        stored = handle.read()
    if stored != payload:
        sys.exit("read-back mismatch")
    words = len(LINE.split())
    print("wrote %s: %d chars, %d words, %d bytes"
          % (path, len(LINE), words, len(payload)))


if __name__ == "__main__":
    main()
