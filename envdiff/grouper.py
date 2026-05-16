"""Group environment variables by prefix or custom mapping."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional


def group_by_prefix(
    env: Dict[str, str],
    delimiter: str = "_",
    depth: int = 1,
) -> Dict[str, Dict[str, str]]:
    """Group keys by their prefix up to *depth* delimiter-separated segments.

    Keys with no delimiter are placed under the empty-string group.
    """
    groups: Dict[str, Dict[str, str]] = defaultdict(dict)
    for key, value in env.items():
        parts = key.split(delimiter)
        if len(parts) <= depth:
            prefix = ""
        else:
            prefix = delimiter.join(parts[:depth])
        groups[prefix][key] = value
    return dict(groups)


def group_by_mapping(
    env: Dict[str, str],
    mapping: Dict[str, List[str]],
    default_group: str = "other",
) -> Dict[str, Dict[str, str]]:
    """Group keys according to an explicit *mapping* of group → list of keys.

    Keys not mentioned in *mapping* are placed in *default_group*.
    """
    reverse: Dict[str, str] = {}
    for group, keys in mapping.items():
        for k in keys:
            reverse[k] = group

    groups: Dict[str, Dict[str, str]] = defaultdict(dict)
    for key, value in env.items():
        group = reverse.get(key, default_group)
        groups[group][key] = value
    return dict(groups)


def group_sizes(groups: Dict[str, Dict[str, str]]) -> Dict[str, int]:
    """Return a mapping of group name → number of keys."""
    return {name: len(keys) for name, keys in groups.items()}


def largest_group(groups: Dict[str, Dict[str, str]]) -> Optional[str]:
    """Return the name of the group with the most keys, or None if empty."""
    if not groups:
        return None
    return max(groups, key=lambda g: len(groups[g]))


def flatten_groups(groups: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    """Merge all groups back into a single flat dict (last write wins on collision)."""
    result: Dict[str, str] = {}
    for members in groups.values():
        result.update(members)
    return result
