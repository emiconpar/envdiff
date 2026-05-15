"""Formatting helpers for tagger output."""

from typing import Dict, List, Optional


def _cyan(text: str, color: bool) -> str:
    return f"\033[36m{text}\033[0m" if color else text


def _bold(text: str, color: bool) -> str:
    return f"\033[1m{text}\033[0m" if color else text


def _yellow(text: str, color: bool) -> str:
    return f"\033[33m{text}\033[0m" if color else text


def format_tag_report(
    tagged: Dict[str, List[str]],
    label: str = "env",
    color: bool = True,
) -> str:
    """Return a human-readable report of key -> tag assignments."""
    lines: List[str] = []
    heading = _bold(f"Tag report: {label}", color)
    lines.append(heading)
    lines.append("-" * 40)

    if not tagged:
        lines.append("  (no keys)")
        return "\n".join(lines)

    for key in sorted(tagged):
        tags = tagged[key]
        key_str = _cyan(key, color)
        if tags:
            tag_str = ", ".join(_yellow(t, color) for t in sorted(tags))
        else:
            tag_str = "(untagged)"
        lines.append(f"  {key_str}: {tag_str}")

    return "\n".join(lines)


def tag_summary(
    tagged: Dict[str, List[str]],
    color: bool = True,
) -> str:
    """Return a one-line summary: total keys, unique tags, untagged count."""
    total = len(tagged)
    unique_tags: set = set()
    untagged = 0
    for tags in tagged.values():
        if tags:
            unique_tags.update(tags)
        else:
            untagged += 1
    parts = [
        f"{total} key(s)",
        f"{len(unique_tags)} unique tag(s)",
        f"{untagged} untagged",
    ]
    return _bold(" | ".join(parts), color)
