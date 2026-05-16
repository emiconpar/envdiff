"""Tests for envdiff.side_by_side_report module."""
import pytest
from envdiff.differ import build_side_by_side
from envdiff.side_by_side_report import (
    format_side_by_side,
    side_by_side_summary,
)


@pytest.fixture
def diff():
    left = {"APP_HOST": "localhost", "APP_PORT": "8080", "OLD_KEY": "gone"}
    right = {"APP_HOST": "prod.host", "APP_PORT": "8080", "NEW_KEY": "here"}
    return build_side_by_side(left, right, left_label="dev", right_label="prod")


def test_format_contains_key(diff):
    output = format_side_by_side(diff, color=False)
    assert "APP_HOST" in output


def test_format_contains_left_label(diff):
    output = format_side_by_side(diff, color=False)
    assert "dev" in output


def test_format_contains_right_label(diff):
    output = format_side_by_side(diff, color=False)
    assert "prod" in output


def test_format_shows_added_key(diff):
    output = format_side_by_side(diff, color=False)
    assert "NEW_KEY" in output


def test_format_shows_removed_key(diff):
    output = format_side_by_side(diff, color=False)
    assert "OLD_KEY" in output


def test_format_shows_dash_for_missing_left(diff):
    output = format_side_by_side(diff, color=False)
    # NEW_KEY has no left value so '-' should appear
    assert "-" in output


def test_format_unchanged_hidden_when_excluded(diff):
    output = format_side_by_side(diff, color=False, include_unchanged=False)
    assert "APP_PORT" not in output


def test_format_unchanged_shown_by_default(diff):
    output = format_side_by_side(diff, color=False)
    assert "APP_PORT" in output


def test_format_with_color_enabled(diff):
    output = format_side_by_side(diff, color=True)
    assert "\033[" in output


def test_format_without_color_no_escape(diff):
    output = format_side_by_side(diff, color=False)
    assert "\033[" not in output


def test_summary_contains_labels(diff):
    summary = side_by_side_summary(diff)
    assert "dev" in summary
    assert "prod" in summary


def test_summary_counts(diff):
    summary = side_by_side_summary(diff)
    assert "+1" in summary
    assert "-1" in summary
    assert "~1" in summary
    assert "=1" in summary
