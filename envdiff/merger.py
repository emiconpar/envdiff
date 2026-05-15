"""Merge multiple env dicts with configurable conflict resolution strategies."""

from typing import Dict, List, Literal, Optional

MergeStrategy = Literal["left", "right", "error", "skip"]


class MergeConflictError(Exception):
    """Raised when a key conflict is found and strategy is 'error'."""

    def __init__(self, key: str, values: List[str]):
        self.key = key
        self.values = values
        super().__init__(
            f"Conflict on key '{key}': {values}"
        )


def merge_envs(
    envs: List[Dict[str, str]],
    strategy: MergeStrategy = "right",
    labels: Optional[List[str]] = None,
) -> Dict[str, str]:
    """Merge a list of env dicts into one.

    Args:
        envs: Ordered list of env dicts to merge.
        strategy: How to handle conflicts.
            - 'left':  first definition wins.
            - 'right': last definition wins (default).
            - 'error': raise MergeConflictError on first conflict.
            - 'skip':  conflicting keys are omitted from result.
        labels: Optional names for each env (used in error messages).

    Returns:
        Merged env dict.
    """
    if not envs:
        return {}

    labels = labels or [str(i) for i in range(len(envs))]
    result: Dict[str, str] = {}
    conflicts: Dict[str, List[str]] = {}

    for env in envs:
        for key, value in env.items():
            if key in result and result[key] != value:
                if strategy == "error":
                    raise MergeConflictError(key, [result[key], value])
                elif strategy == "left":
                    pass  # keep existing
                elif strategy == "right":
                    result[key] = value
                elif strategy == "skip":
                    conflicts.setdefault(key, [result[key]])
                    conflicts[key].append(value)
            else:
                result[key] = value

    for key in conflicts:
        result.pop(key, None)

    return result


def merge_conflicts(
    envs: List[Dict[str, str]],
) -> Dict[str, List[str]]:
    """Return a mapping of keys that differ across envs to their distinct values."""
    seen: Dict[str, List[str]] = {}
    for env in envs:
        for key, value in env.items():
            seen.setdefault(key, [])
            if value not in seen[key]:
                seen[key].append(value)
    return {k: v for k, v in seen.items() if len(v) > 1}
