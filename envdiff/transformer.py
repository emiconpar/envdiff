"""Transform environment variable dicts: rename keys, remap values, apply custom functions."""

from typing import Callable, Dict, Optional


def rename_keys(env: Dict[str, str], mapping: Dict[str, str]) -> Dict[str, str]:
    """Return a new env dict with keys renamed according to mapping.

    Keys not in mapping are kept as-is. If a target name already exists
    and is not being renamed, the renamed value takes precedence.
    """
    result = {}
    rename_targets = set(mapping.values())
    for key, value in env.items():
        if key in mapping:
            result[mapping[key]] = value
        elif key not in rename_targets:
            result[key] = value
    return result


def remap_values(env: Dict[str, str], mapping: Dict[str, str]) -> Dict[str, str]:
    """Return a new env dict with values substituted according to mapping.

    Only exact value matches are replaced. Keys are unchanged.
    """
    return {k: mapping.get(v, v) for k, v in env.items()}


def apply_transform(env: Dict[str, str], fn: Callable[[str, str], Optional[tuple]]) -> Dict[str, str]:
    """Apply a callable to each (key, value) pair.

    The callable receives (key, value) and should return a (new_key, new_value)
    tuple, or None to drop the entry from the result.
    """
    result = {}
    for key, value in env.items():
        out = fn(key, value)
        if out is not None:
            new_key, new_value = out
            result[new_key] = new_value
    return result


def prefix_keys(env: Dict[str, str], prefix: str) -> Dict[str, str]:
    """Return a new env dict with *prefix* prepended to every key."""
    return {f"{prefix}{k}": v for k, v in env.items()}


def strip_key_prefix(env: Dict[str, str], prefix: str) -> Dict[str, str]:
    """Return a new env dict with *prefix* removed from matching keys.

    Keys that do not start with the prefix are kept unchanged.
    """
    result = {}
    for key, value in env.items():
        if key.startswith(prefix):
            result[key[len(prefix):]] = value
        else:
            result[key] = value
    return result


def uppercase_keys(env: Dict[str, str]) -> Dict[str, str]:
    """Return a new env dict with all keys converted to uppercase."""
    return {k.upper(): v for k, v in env.items()}


def lowercase_values(env: Dict[str, str]) -> Dict[str, str]:
    """Return a new env dict with all values converted to lowercase."""
    return {k: v.lower() for k, v in env.items()}
