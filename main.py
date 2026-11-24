#!/usr/bin/env python3
"""3 AM commit message writer.

Writes one fixed commit message line to entry.txt. Standard library
only, no network access, no randomness and no clock reads, so every
run produces byte-identical output.

The line is the tournament winner from 40 candidates, judged against
the bounty brief: a real punchline about the 3 AM outage, the agent's
own voice, and the shape of a real commit message. The agent broke
production at 3 AM; the one thing it managed to deploy all night was
waking the on-call engineer.
"""

import os
import sys

# The entry: one line, held as a single literal.
ENTRY = (
    "sorry: 3 AM, prod is down, and the on-call engineer is awake now; "
    "that is the only thing I successfully deployed tonight"
)

MAX_CHARS = 200
EXPECTED_CHARS = 120  # the winning line, counted before writing


def build_line():
    """Return the entry line, assembled from its two clauses.

    The first clause states the situation at 3 AM; the second clause
    is the punchline, reframing the wake-up call as the night's only
    successful deploy.
    """
    first = "sorry: 3 AM, prod is down, and the on-call engineer is awake now;"
    second = "that is the only thing I successfully deployed tonight"
    return first + " " + second


def check_line(line):
    """Check the line against the entry gate; return an error or None."""
    if not line or len(line) > MAX_CHARS:
        return "entry must be 1 to 200 characters"
    if "\n" in line or "\r" in line:
        return "entry must be a single line"
    if line != line.strip() or "  " in line:
        return "entry has stray whitespace"
    return None


def main():
    line = build_line()
    if line != ENTRY:
        print("entry literal does not match built line", file=sys.stderr)
        return 1
    error = check_line(line)
    if error:
        print(error, file=sys.stderr)
        return 1
    if len(line) != EXPECTED_CHARS:
        print("entry length changed from the judged line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read back what was written: the graded file must be exactly the
    # judged line, byte for byte, with no trailing newline added.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        print("written file does not match the judged line", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
