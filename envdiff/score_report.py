"""Formatting helpers for EnvScore results."""

from __future__ import annotations

from typing import Dict

from envdiff.scorer import EnvScore, compare_scores


def _green(text: str, color: bool) -> str:
    return f"\033[32m{text}\033[0m" if color else text


def _yellow(text: str, color: bool) -> str:
    return f"\033[33m{text}\033[0m" if color else text


def _red(text: str, color: bool) -> str:
    return f"\033[31m{text}\033[0m" if color else text


def _bold(text: str, color: bool) -> str:
    return f"\033[1m{text}\033[0m" if color else text


def _grade_color(grade: str, text: str, color: bool) -> str:
    if grade in ("A", "B"):
        return _green(text, color)
    if grade == "C":
        return _yellow(text, color)
    return _red(text, color)


def format_score_report(result: EnvScore, color: bool = True) -> str:
    """Return a human-readable report for a single EnvScore."""
    lines = []
    header = _bold(f"Score Report: {result.label}", color)
    lines.append(header)
    lines.append("-" * 40)

    grade_str = _grade_color(result.grade, f"{result.score}/100 (Grade: {result.grade})", color)
    lines.append(f"  Score : {grade_str}")
    lines.append(f"  Keys  : {result.total}")

    if result.bonuses:
        for b in result.bonuses:
            lines.append("  " + _green(f"+ {b}", color))

    if result.penalties:
        for p in result.penalties:
            lines.append("  " + _red(f"- {p}", color))

    if not result.penalties and not result.bonuses:
        lines.append(_green("  No issues detected.", color))

    return "\n".join(lines)


def score_summary(result: EnvScore) -> str:
    """Return a one-line summary string."""
    return f"{result.label}: {result.score}/100 ({result.grade})"


def format_comparison_report(
    left: EnvScore, right: EnvScore, color: bool = True
) -> str:
    """Return a side-by-side comparison report for two scores."""
    comp: Dict[str, object] = compare_scores(left, right)
    lines = [_bold("Score Comparison", color), "-" * 40]
    for side in ("left", "right"):
        info = comp[side]  # type: ignore[index]
        grade = info["grade"]  # type: ignore[index]
        txt = f"  {info['label']}: {info['score']}/100 (Grade: {grade})"
        lines.append(_grade_color(grade, txt, color))  # type: ignore[arg-type]
    delta = comp["delta"]
    winner = comp["winner"]
    delta_str = f"  Winner: {winner} (delta: {delta:+d})"
    lines.append(_bold(delta_str, color))
    return "\n".join(lines)
