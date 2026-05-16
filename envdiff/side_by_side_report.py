"""Formatter for side-by-side diff output."""
from __future__ import annotations

from typing import Optional

from envdiff.differ import SideBySideDiff, SideBySideRow

_COL_WIDTH = 36


def _green(text: str) -> str:
    return f"\033[32m{text}\033[0m"


def _red(text: str) -> str:
    return f"\033[31m{text}\033[0m"


def _yellow(text: str) -> str:
    return f"\033[33m{text}\033[0m"


def _dim(text: str) -> str:
    return f"\033[2m{text}\033[0m"


def _bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def _cell(value: Optional[str], width: int = _COL_WIDTH) -> str:
    if value is None:
        return "-".center(width)
    display = value if len(value) <= width else value[: width - 3] + "..."
    return display.ljust(width)


def format_side_by_side(
    diff: SideBySideDiff,
    color: bool = True,
    include_unchanged: bool = True,
) -> str:
    lines = []
    sep = "-" * (_COL_WIDTH * 2 + 20)
    header = f"{'KEY':<20}  {diff.left_label:<{_COL_WIDTH}}  {diff.right_label:<{_COL_WIDTH}}"
    lines.append(_bold(header) if color else header)
    lines.append(sep)

    for row in diff.rows:
        if row.status == "unchanged" and not include_unchanged:
            continue
        left_cell = _cell(row.left_value)
        right_cell = _cell(row.right_value)
        key_col = f"{row.key:<20}"
        line = f"{key_col}  {left_cell}  {right_cell}"
        if color:
            if row.status == "added":
                line = _green(line)
            elif row.status == "removed":
                line = _red(line)
            elif row.status == "changed":
                line = _yellow(line)
            else:
                line = _dim(line)
        lines.append(line)

    lines.append(sep)
    return "\n".join(lines)


def side_by_side_summary(diff: SideBySideDiff) -> str:
    a = len(diff.added())
    r = len(diff.removed())
    c = len(diff.changed())
    u = len(diff.unchanged())
    return (
        f"Side-by-side [{diff.left_label} vs {diff.right_label}]: "
        f"+{a} added, -{r} removed, ~{c} changed, ={u} unchanged"
    )
