"""Detect and resolve duplicate or shadowed keys across multiple env sources."""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class DeduplicationResult:
    """Result of a deduplication pass over multiple env dicts."""

    label: str
    duplicates: Dict[str, List[Tuple[int, str]]]  # key -> [(source_index, value), ...]
    resolved: Dict[str, str]
    strategy: str

    @property
    def has_duplicates(self) -> bool:
        return bool(self.duplicates)

    @property
    def duplicate_count(self) -> int:
        return len(self.duplicates)


def find_duplicates(
    envs: List[Dict[str, str]]
) -> Dict[str, List[Tuple[int, str]]]:
    """Return keys that appear in more than one env with differing values."""
    seen: Dict[str, List[Tuple[int, str]]] = {}
    for idx, env in enumerate(envs):
        for key, value in env.items():
            seen.setdefault(key, []).append((idx, value))
    return {
        key: entries
        for key, entries in seen.items()
        if len(entries) > 1 and len({v for _, v in entries}) > 1
    }


def deduplicate(
    envs: List[Dict[str, str]],
    strategy: str = "last",
    label: str = "deduplication",
) -> DeduplicationResult:
    """Merge multiple env dicts, resolving duplicate keys by strategy.

    Strategies:
      - 'last'  : last source wins (default)
      - 'first' : first source wins
      - 'error' : raise ValueError on any conflict
    """
    if strategy not in ("last", "first", "error"):
        raise ValueError(f"Unknown strategy: {strategy!r}")

    duplicates = find_duplicates(envs)

    if strategy == "error" and duplicates:
        conflicting = ", ".join(sorted(duplicates))
        raise ValueError(f"Duplicate keys detected: {conflicting}")

    merged: Dict[str, str] = {}
    sources = envs if strategy == "last" else list(reversed(envs))
    for env in sources:
        merged.update(env)

    if strategy == "first":
        # rebuild so first-seen value is kept
        merged = {}
        for env in envs:
            for key, value in env.items():
                if key not in merged:
                    merged[key] = value

    return DeduplicationResult(
        label=label,
        duplicates=duplicates,
        resolved=merged,
        strategy=strategy,
    )
