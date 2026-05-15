"""Tests for envdiff.profile_report."""

import pytest
from envdiff.profiler import profile_env
from envdiff.profile_report import (
    format_profile_report,
    profile_summary,
    format_comparison_report,
)


@pytest.fixture
def sample_profile():
    env = {
        "APP_HOST": "localhost",
        "APP_PORT": "8080",
        "DB_HOST": "db.local",
        "DB_PASS": "",
    }
    return profile_env(env, label="staging")


def test_format_report_contains_label(sample_profile):
    report = format_profile_report(sample_profile, color=False)
    assert "staging" in report


def test_format_report_shows_total_keys(sample_profile):
    report = format_profile_report(sample_profile, color=False)
    assert "4" in report


def test_format_report_shows_empty_values(sample_profile):
    report = format_profile_report(sample_profile, color=False)
    assert "DB_PASS" in report


def test_format_report_shows_top_prefixes(sample_profile):
    report = format_profile_report(sample_profile, color=False)
    assert "APP" in report
    assert "DB" in report


def test_format_report_color_disabled(sample_profile):
    report = format_profile_report(sample_profile, color=False)
    assert "\033[" not in report


def test_format_report_color_enabled(sample_profile):
    report = format_profile_report(sample_profile, color=True)
    assert "\033[" in report


def test_profile_summary_contains_label(sample_profile):
    summary = profile_summary(sample_profile)
    assert "staging" in summary


def test_profile_summary_contains_key_count(sample_profile):
    summary = profile_summary(sample_profile)
    assert "4 keys" in summary


def test_profile_summary_contains_empty_count(sample_profile):
    summary = profile_summary(sample_profile)
    assert "1 empty" in summary


def test_format_comparison_report_contains_both_labels():
    left = profile_env({"A": "1", "B": ""}, label="dev")
    right = profile_env({"A": "1", "C": "3", "D": "4"}, label="prod")
    report = format_comparison_report(left, right, color=False)
    assert "dev" in report
    assert "prod" in report


def test_format_comparison_report_shows_total_keys():
    left = profile_env({"A": "1"}, label="l")
    right = profile_env({"A": "1", "B": "2", "C": "3"}, label="r")
    report = format_comparison_report(left, right, color=False)
    assert "1" in report
    assert "3" in report
