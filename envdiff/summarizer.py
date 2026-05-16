"""Summarizer: produce a concise statistical summary of an env dict."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EnvSummary:
    label: str
    total: int
    empty_count: int
    unique_prefixes: List[str]
    longest_key: str
    shortest_key: str
    longest_value_key: str
    avg_value_length: float
    prefix_counts: Dict[str, int] = field(default_factory=dict)


def summarize_env(env: Dict[str, str], label: str = "env") -> EnvSummary:
    """Return an EnvSummary for *env*."""
    if not env:
        return EnvSummary(
            label=label,
            total=0,
            empty_count=0,
            unique_prefixes=[],
            longest_key="",
            shortest_key="",
            longest_value_key="",
            avg_value_length=0.0,
            prefix_counts={},
        )

    keys = list(env.keys())
    empty_count = sum(1 for v in env.values() if v == "")

    prefix_counts: Dict[str, int] = {}
    for k in keys:
        prefix = k.split("_")[0] if "_" in k else k
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1

    unique_prefixes = sorted(prefix_counts.keys())
    longest_key = max(keys, key=len)
    shortest_key = min(keys, key=len)
    longest_value_key = max(env, key=lambda k: len(env[k]))
    avg_value_length = sum(len(v) for v in env.values()) / len(env)

    return EnvSummary(
        label=label,
        total=len(env),
        empty_count=empty_count,
        unique_prefixes=unique_prefixes,
        longest_key=longest_key,
        shortest_key=shortest_key,
        longest_value_key=longest_value_key,
        avg_value_length=round(avg_value_length, 2),
        prefix_counts=prefix_counts,
    )


def compare_summaries(a: EnvSummary, b: EnvSummary) -> Dict[str, object]:
    """Return a dict highlighting numeric differences between two summaries."""
    return {
        "total_delta": b.total - a.total,
        "empty_delta": b.empty_count - a.empty_count,
        "prefix_count_delta": len(b.unique_prefixes) - len(a.unique_prefixes),
        "avg_value_length_delta": round(b.avg_value_length - a.avg_value_length, 2),
        "labels": (a.label, b.label),
    }
