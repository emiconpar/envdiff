"""Core diffing logic for comparing two environment variable sets."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class EnvDiffResult:
    """Result of comparing two environment variable sets."""

    only_in_left: Dict[str, str] = field(default_factory=dict)
    only_in_right: Dict[str, str] = field(default_factory=dict)
    changed: Dict[str, tuple] = field(default_factory=dict)  # key -> (left_val, right_val)
    unchanged: Dict[str, str] = field(default_factory=dict)

    @property
    def has_differences(self) -> bool:
        return bool(self.only_in_left or self.only_in_right or self.changed)

    @property
    def summary(self) -> str:
        parts: List[str] = []
        if self.only_in_left:
            parts.append(f"{len(self.only_in_left)} only in left")
        if self.only_in_right:
            parts.append(f"{len(self.only_in_right)} only in right")
        if self.changed:
            parts.append(f"{len(self.changed)} changed")
        if self.unchanged:
            parts.append(f"{len(self.unchanged)} unchanged")
        return ", ".join(parts) if parts else "no variables found"


def diff_envs(
    left: Dict[str, str],
    right: Dict[str, str],
    ignore_keys: Optional[List[str]] = None,
) -> EnvDiffResult:
    """Compare two environment variable dictionaries.

    Args:
        left: First env set (e.g. from a .env file).
        right: Second env set (e.g. from a running process).
        ignore_keys: Optional list of keys to exclude from comparison.

    Returns:
        An EnvDiffResult describing the differences.
    """
    ignored = set(ignore_keys or [])
    left_filtered = {k: v for k, v in left.items() if k not in ignored}
    right_filtered = {k: v for k, v in right.items() if k not in ignored}

    left_keys = set(left_filtered)
    right_keys = set(right_filtered)

    result = EnvDiffResult()
    result.only_in_left = {k: left_filtered[k] for k in left_keys - right_keys}
    result.only_in_right = {k: right_filtered[k] for k in right_keys - left_keys}

    for key in left_keys & right_keys:
        lv, rv = left_filtered[key], right_filtered[key]
        if lv != rv:
            result.changed[key] = (lv, rv)
        else:
            result.unchanged[key] = lv

    return result
