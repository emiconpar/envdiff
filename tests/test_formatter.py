"""Tests for envdiff.formatter module."""

import pytest
from envdiff.diff import EnvDiffResult, diff_envs
from envdiff.formatter import format_diff, format_summary


@pytest.fixture
def sample_result():
    left = {"A": "1", "B": "old", "C": "same"}
    right = {"B": "new", "C": "same", "D": "4"}
    return diff_envs(left, right)


def test_format_diff_contains_removed_key(sample_result):
    output = format_diff(sample_result, use_color=False)
    assert "- A=1" in output


def test_format_diff_contains_added_key(sample_result):
    output = format_diff(sample_result, use_color=False)
    assert "+ D=4" in output


def test_format_diff_contains_changed_values(sample_result):
    output = format_diff(sample_result, use_color=False)
    assert "- B=old" in output
    assert "+ B=new" in output


def test_format_diff_labels_appear(sample_result):
    output = format_diff(sample_result, left_label=".env", right_label="prod", use_color=False)
    assert "--- .env" in output
    assert "+++ prod" in output


def test_format_diff_no_unchanged_by_default(sample_result):
    output = format_diff(sample_result, use_color=False)
    assert "C=same" not in output


def test_format_diff_show_unchanged(sample_result):
    output = format_diff(sample_result, use_color=False, show_unchanged=True)
    assert "C=same" in output


def test_format_diff_no_differences():
    result = diff_envs({"X": "1"}, {"X": "1"})
    output = format_diff(result, use_color=False)
    assert "No differences found." in output


def test_format_summary_removed(sample_result):
    output = format_summary(sample_result, use_color=False)
    assert "removed" in output


def test_format_summary_added(sample_result):
    output = format_summary(sample_result, use_color=False)
    assert "added" in output


def test_format_summary_changed(sample_result):
    output = format_summary(sample_result, use_color=False)
    assert "changed" in output


def test_format_summary_no_differences():
    result = diff_envs({"A": "1"}, {"A": "1"})
    output = format_summary(result, use_color=False)
    assert "No differences." in output


def test_format_diff_with_color_contains_ansi(sample_result):
    output = format_diff(sample_result, use_color=True)
    assert "\033[" in output


def test_format_diff_without_color_no_ansi(sample_result):
    output = format_diff(sample_result, use_color=False)
    assert "\033[" not in output
