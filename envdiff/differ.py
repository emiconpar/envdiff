"""Side-by-side diff renderer for environment variable sets."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from envdiff.diff import EnvDiffResult, diff_envs


@dataclass
class SideBySideRow:
    key: str
    left_value: Optional[str]
    right_value: Optional[str]
    status: str  # 'added' | 'removed' | 'changed' | 'unchanged'


@dataclass
class SideBySideDiff:
    rows: List[SideBySideRow] = field(default_factory=list)
    left_label: str = "left"
    right_label: str = "right"

    def added(self) -> List[SideBySideRow]:
        return [r for r in self.rows if r.status == "added"]

    def removed(self) -> List[SideBySideRow]:
        return [r for r in self.rows if r.status == "removed"]

    def changed(self) -> List[SideBySideRow]:
        return [r for r in self.rows if r.status == "changed"]

    def unchanged(self) -> List[SideBySideRow]:
        return [r for r in self.rows if r.status == "unchanged"]


def build_side_by_side(
    left: Dict[str, str],
    right: Dict[str, str],
    left_label: str = "left",
    right_label: str = "right",
    include_unchanged: bool = True,
) -> SideBySideDiff:
    """Build a SideBySideDiff from two env dicts."""
    result: EnvDiffResult = diff_envs(left, right)
    rows: List[SideBySideRow] = []

    all_keys = sorted(
        set(left) | set(right)
    )

    for key in all_keys:
        if key in result.only_in_right:
            rows.append(SideBySideRow(key, None, right[key], "added"))
        elif key in result.only_in_left:
            rows.append(SideBySideRow(key, left[key], None, "removed"))
        elif key in result.changed:
            lv, rv = result.changed[key]
            rows.append(SideBySideRow(key, lv, rv, "changed"))
        else:
            if include_unchanged:
                rows.append(SideBySideRow(key, left[key], right[key], "unchanged"))

    return SideBySideDiff(rows=rows, left_label=left_label, right_label=right_label)
