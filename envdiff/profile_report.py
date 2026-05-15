"""Render human-readable reports for EnvProfile objects."""

from __future__ import annotations

from typing import Optional

from envdiff.profiler import EnvProfile, compare_profiles


def _bold(text: str, color: bool) -> str:
    return f"\033[1m{text}\033[0m" if color else text


def _cyan(text: str, color: bool) -> str:
    return f"\033[36m{text}\033[0m" if color else text


def format_profile_report(profile: EnvProfile, color: bool = True) -> str:
    """Format a single EnvProfile as a readable report string."""
    lines = []
    lines.append(_bold(f"Profile: {profile.label}", color))
    lines.append(f"  Total keys     : {profile.total_keys}")
    lines.append(f"  Empty values   : {len(profile.empty_values)}")
    if profile.empty_values:
        lines.append(f"    Keys         : {', '.join(profile.empty_values)}")
    lines.append(f"  Longest key    : {profile.longest_key}")
    lines.append(f"  Longest value  : {profile.longest_value_key}")
    if profile.top_prefixes:
        lines.append("  Top prefixes:")
        for prefix, count in profile.top_prefixes:
            lines.append(f"    {_cyan(prefix, color)}: {count}")
    return "\n".join(lines)


def profile_summary(profile: EnvProfile) -> str:
    """One-line summary of a profile."""
    return (
        f"{profile.label}: {profile.total_keys} keys, "
        f"{len(profile.empty_values)} empty, "
        f"{len(profile.prefixes)} prefix groups"
    )


def format_comparison_report(
    left: EnvProfile,
    right: EnvProfile,
    color: bool = True,
) -> str:
    """Format a side-by-side comparison of two profiles."""
    cmp = compare_profiles(left, right)
    lines = [_bold("Profile Comparison", color)]
    for metric, values in cmp.items():
        label_l, label_r = list(values.keys())
        lines.append(f"  {metric}:")
        lines.append(f"    {label_l}: {values[label_l]}")
        lines.append(f"    {label_r}: {values[label_r]}")
    return "\n".join(lines)
