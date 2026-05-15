"""Utilities for sorting and ordering environment variable dictionaries."""

from typing import Dict, List, Optional


def sort_env_keys(
    env: Dict[str, str],
    reverse: bool = False,
) -> Dict[str, str]:
    """Return a new dict with keys sorted alphabetically."""
    return dict(sorted(env.items(), key=lambda kv: kv[0], reverse=reverse))


def sort_env_by_value(
    env: Dict[str, str],
    reverse: bool = False,
) -> Dict[str, str]:
    """Return a new dict with entries sorted by value."""
    return dict(sorted(env.items(), key=lambda kv: kv[1], reverse=reverse))


def sort_env_by_prefix(
    env: Dict[str, str],
    prefixes: List[str],
) -> Dict[str, str]:
    """Return a new dict with keys grouped by prefix order, remainder appended.

    Keys matching the first prefix come first, then the second, and so on.
    Keys not matching any prefix are appended at the end, sorted alphabetically.
    """

    def _priority(key: str) -> int:
        for idx, prefix in enumerate(prefixes):
            if key.startswith(prefix):
                return idx
        return len(prefixes)

    return dict(
        sorted(env.items(), key=lambda kv: (_priority(kv[0]), kv[0]))
    )


def top_n_keys(
    env: Dict[str, str],
    n: int,
    by: str = "key",
) -> Dict[str, str]:
    """Return the first *n* entries after sorting.

    Args:
        env: Source environment dict.
        n: Maximum number of entries to return.
        by: Sort criterion – ``'key'`` (default) or ``'value'``.

    Raises:
        ValueError: If *by* is not ``'key'`` or ``'value'``.
    """
    if by == "key":
        ordered = sort_env_keys(env)
    elif by == "value":
        ordered = sort_env_by_value(env)
    else:
        raise ValueError(f"Unknown sort criterion: {by!r}. Use 'key' or 'value'.")
    return dict(list(ordered.items())[:n])
