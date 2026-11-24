#!/usr/bin/env python3
"""Write the out-of-office reply to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 160 characters, not only white space.
"""

import os
import sys
from pathlib import Path

ENTRY = (
    'I am on vacation. My inbox is now run by a toaster with strong opinions and no password. Expect delays, crumbs, and silence.'
)

MIN_CHARS = 1
MAX_CHARS = 160
DEFAULT_PATH = "/output/entry.txt"


def gate_error(text: str) -> str | None:
    """Return why the entry fails the competition gate, or None if it passes."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return f"entry is {len(text)} characters, gate is {MIN_CHARS} to {MAX_CHARS}"
    if not text.strip():
        return "entry is only white space"
    if "\n" in text:
        return "entry must be one line"
    return None


def resolve_output_path() -> Path:
    """Pick the output path: first argument, $OUTPUT_PATH, or the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return Path(os.environ.get("OUTPUT_PATH", DEFAULT_PATH))


def main() -> int:
    text = ENTRY
    error = gate_error(text)
    if error is not None:
        print(error, file=sys.stderr)
        return 1
    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
