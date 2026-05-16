"""Tests for envdiff.mask_report."""

import pytest
from envdiff.masker import mask_env
from envdiff.mask_report import format_mask_report, masking_summary


@pytest.fixture
def original() -> dict[str, str]:
    return {
        "APP_NAME": "myapp",
        "DB_PASSWORD": "supersecret",
        "API_KEY": "abc123",
    }


@pytest.fixture
def masked(original) -> dict[str, str]:
    return mask_env(original, {"DB_PASSWORD", "API_KEY"})


def test_format_report_contains_label(masked, original):
    report = format_mask_report(masked, original, label="production")
    assert "production" in report


def test_format_report_shows_masked_count(masked, original):
    report = format_mask_report(masked, original, color=False)
    assert "2" in report


def test_format_report_lists_masked_keys(masked, original):
    report = format_mask_report(masked, original, color=False)
    assert "DB_PASSWORD" in report
    assert "API_KEY" in report


def test_format_report_no_masking_message(original):
    report = format_mask_report(original, original, color=False)
    assert "No keys masked" in report


def test_format_report_color_disabled(masked, original):
    report = format_mask_report(masked, original, color=False)
    assert "\033[" not in report


def test_format_report_color_enabled(masked, original):
    report = format_mask_report(masked, original, color=True)
    assert "\033[" in report


def test_masking_summary_some_masked(masked, original):
    summary = masking_summary(masked, original)
    assert "2/3" in summary
    assert "masked" in summary


def test_masking_summary_none_masked(original):
    summary = masking_summary(original, original)
    assert "No keys masked" in summary


def test_masking_summary_total_count(masked, original):
    summary = masking_summary(masked, original)
    assert "3" in summary
