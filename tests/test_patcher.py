"""Tests for envdiff.patcher and envdiff.patch_report."""

import pytest
from envdiff.diff import diff_envs
from envdiff.patcher import apply_patch, revert_patch, patch_summary, PatchError
from envdiff.patch_report import format_patch_report, patch_summary_line


@pytest.fixture()
def left():
    return {"A": "1", "B": "2", "C": "old"}


@pytest.fixture()
def right():
    return {"A": "1", "C": "new", "D": "4"}


@pytest.fixture()
def diff(left, right):
    return diff_envs(left, right)


# --- apply_patch ---

def test_apply_patch_adds_only_in_right(left, diff):
    result = apply_patch(left, diff)
    assert result["D"] == "4"


def test_apply_patch_removes_only_in_left(left, diff):
    result = apply_patch(left, diff)
    assert "B" not in result


def test_apply_patch_right_strategy_takes_new_value(left, diff):
    result = apply_patch(left, diff, strategy="right")
    assert result["C"] == "new"


def test_apply_patch_left_strategy_keeps_base_value(left, diff):
    result = apply_patch(left, diff, strategy="left")
    assert result["C"] == "old"


def test_apply_patch_left_strategy_still_adds_new_keys(left, diff):
    result = apply_patch(left, diff, strategy="left")
    assert result["D"] == "4"


def test_apply_patch_error_strategy_raises_on_conflict(left, diff):
    with pytest.raises(PatchError, match="C"):
        apply_patch(left, diff, strategy="error")


def test_apply_patch_invalid_strategy_raises(left, diff):
    with pytest.raises(ValueError):
        apply_patch(left, diff, strategy="unknown")


def test_apply_patch_no_conflict_error_strategy_succeeds():
    base = {"X": "1"}
    d = diff_envs(base, {"X": "1", "Y": "2"})
    result = apply_patch(base, d, strategy="error")
    assert result["Y"] == "2"


# --- revert_patch ---

def test_revert_patch_restores_original(left, right, diff):
    patched = apply_patch(left, diff)
    reverted = revert_patch(patched, diff)
    assert reverted == left


def test_revert_patch_removes_added_keys(left, diff):
    patched = apply_patch(left, diff)
    reverted = revert_patch(patched, diff)
    assert "D" not in reverted


# --- patch_summary ---

def test_patch_summary_counts(diff):
    s = patch_summary(diff)
    assert s["additions"] == 1
    assert s["deletions"] == 1
    assert s["modifications"] == 1


# --- format_patch_report ---

def test_format_patch_report_contains_label(diff):
    report = format_patch_report(diff, label="my-patch", color=False)
    assert "my-patch" in report


def test_format_patch_report_shows_addition(diff):
    report = format_patch_report(diff, color=False)
    assert "+ D=4" in report


def test_format_patch_report_shows_deletion(diff):
    report = format_patch_report(diff, color=False)
    assert "- B" in report


def test_format_patch_report_shows_modification(diff):
    report = format_patch_report(diff, color=False)
    assert "~ C" in report


def test_format_patch_report_noop_message():
    env = {"A": "1"}
    d = diff_envs(env, env)
    report = format_patch_report(d, color=False)
    assert "no-op" in report.lower()


# --- patch_summary_line ---

def test_patch_summary_line_contains_added(diff):
    line = patch_summary_line(diff, color=False)
    assert "+1 added" in line


def test_patch_summary_line_contains_removed(diff):
    line = patch_summary_line(diff, color=False)
    assert "-1 removed" in line


def test_patch_summary_line_contains_modified(diff):
    line = patch_summary_line(diff, color=False)
    assert "~1 modified" in line
