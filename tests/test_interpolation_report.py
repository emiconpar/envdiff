"""Tests for envdiff.interpolation_report."""

from envdiff.interpolation_report import (
    format_interpolation_report,
    interpolation_summary,
)


def test_report_shows_label():
    report = format_interpolation_report({}, {}, {}, label="myenv", color=False)
    assert "myenv" in report


def test_report_shows_resolved_key():
    original = {"PATH": "${BASE}/bin"}
    interpolated = {"PATH": "/usr/bin"}
    report = format_interpolation_report(original, interpolated, {}, color=False)
    assert "PATH" in report
    assert "/usr/bin" in report


def test_report_no_changes_message():
    env = {"KEY": "value"}
    report = format_interpolation_report(env, env, {}, color=False)
    assert "No substitutions" in report


def test_report_shows_unresolved_key():
    env = {"X": "${MISSING}"}
    unresolved = {"X": ["MISSING"]}
    report = format_interpolation_report(env, env, unresolved, color=False)
    assert "MISSING" in report
    assert "Unresolved" in report


def test_report_color_disabled():
    env = {"A": "${B}"}
    interp = {"A": "resolved"}
    report = format_interpolation_report(env, interp, {}, color=False)
    assert "\033[" not in report


def test_report_color_enabled():
    env = {"A": "${B}"}
    interp = {"A": "resolved"}
    report = format_interpolation_report(env, interp, {}, color=True)
    assert "\033[" in report


def test_summary_all_resolved():
    summary = interpolation_summary({}, color=False)
    assert "All references resolved" in summary


def test_summary_with_unresolved():
    unresolved = {"KEY": ["MISSING"]}
    summary = interpolation_summary(unresolved, color=False)
    assert "unresolved" in summary.lower()
    assert "1" in summary


def test_summary_counts_references():
    unresolved = {"K1": ["A", "B"], "K2": ["C"]}
    summary = interpolation_summary(unresolved, color=False)
    assert "3" in summary
    assert "2" in summary


def test_summary_color_disabled():
    summary = interpolation_summary({"X": ["Y"]}, color=False)
    assert "\033[" not in summary
