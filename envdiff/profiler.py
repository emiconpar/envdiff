"""Profile environment variable sets: count keys, detect patterns, and summarize statistics."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class EnvProfile:
    label: str
    total_keys: int
    empty_values: List[str] = field(default_factory=list)
    prefixes: Dict[str, int] = field(default_factory=dict)
    longest_key: str = ""
    longest_value_key: str = ""
    top_prefixes: List[Tuple[str, int]] = field(default_factory=list)


def profile_env(env: Dict[str, str], label: str = "env", top_n: int = 5) -> EnvProfile:
    """Compute a statistical profile of an environment variable mapping."""
    if not env:
        return EnvProfile(label=label, total_keys=0)

    empty_values = [k for k, v in env.items() if v == ""]

    prefix_counter: Counter = Counter()
    for key in env:
        parts = key.split("_", 1)
        if len(parts) > 1:
            prefix_counter[parts[0]] += 1

    longest_key = max(env.keys(), key=len)
    longest_value_key = max(env.keys(), key=lambda k: len(env[k]))

    top_prefixes = prefix_counter.most_common(top_n)

    return EnvProfile(
        label=label,
        total_keys=len(env),
        empty_values=empty_values,
        prefixes=dict(prefix_counter),
        longest_key=longest_key,
        longest_value_key=longest_value_key,
        top_prefixes=top_prefixes,
    )


def compare_profiles(left: EnvProfile, right: EnvProfile) -> Dict[str, object]:
    """Return a simple comparison dict between two EnvProfile instances."""
    return {
        "total_keys": {left.label: left.total_keys, right.label: right.total_keys},
        "empty_values": {left.label: len(left.empty_values), right.label: len(right.empty_values)},
        "unique_prefixes": {left.label: len(left.prefixes), right.label: len(right.prefixes)},
    }
