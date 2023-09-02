"""Currently only handles CRLF and LF conversion."""
from __future__ import annotations

import argparse
from enum import Enum
from pathlib import Path


class LineEnding(Enum):
    CRLF = "\r\n"
    LF = "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path)
    parser.add_argument("--to", choices=["crlf", "lf"])

    args = parser.parse_args()
    # TODO(cnpryer): Default better and use argparse to parse as
    line_ending = LineEnding.LF
    match args.to.lower():
        case "lf":
            line_ending = LineEnding.LF
        case "CRLF":
            line_ending = LineEnding.CRLF

    count = 0
    for path in args.path.glob("./**/*.py"):
        contents, converted = convert_line_endings(path, line_ending)
        open(path, "w").write(contents)
        if converted:
            count += 1
    print(f"converted {count} files")


# TODO(cnpryer): Detect
def convert_line_endings(path: Path, line_ending: LineEnding) -> (str, bool):
    contents = open(path, "r").read()
    match line_ending:
        case LineEnding.LF:
            return contents.replace("\r\n", LineEnding.LF.value), True
        case LineEnding.CRLF:
            return contents.replace("\n", LineEnding.CRLF.value), True
    return contents, False

if __name__ == "__main__":
    main()