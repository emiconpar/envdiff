"""Tests for envdiff.validation_reporter."""

from envdiff.validator import ValidationResult
from envdiff.validation_reporter import (
    format_validation_report,
    validation_summary,
)


# ---------------------------------------------------------------------------
# format_validation_report
# ---------------------------------------------------------------------------

def test_report_clean_contains_ok():
    result = ValidationResult()
    report = format_validation_report(result, color=False)
    assert "OK" in report


def test_report_includes_label():
    result = ValidationResult()
    report = format_validation_report(result, label=".env.prod", color=False)
    assert ".env.prod" in report


def test_report_shows_errors():
    result = ValidationResult(errors=["Missing required key: 'SECRET'"])
    report = format_validation_report(result, color=False)
    assert "ERROR" in report
    assert "SECRET" in report


def test_report_shows_warnings():
    result = ValidationResult(warnings=["Key has empty value: 'DEBUG'"])
    report = format_validation_report(result, color=False)
    assert "WARN" in report
    assert "DEBUG" in report


def test_report_shows_both_errors_and_warnings():
    result = ValidationResult(
        errors=["Missing required key: 'DB_URL'"],
        warnings=["Key has empty value: 'LOG_LEVEL'"],
    )
    report = format_validation_report(result, color=False)
    assert "ERROR" in report
    assert "WARN" in report


def test_report_color_codes_present_by_default():
    result = ValidationResult(errors=["bad key"])
    report = format_validation_report(result)
    assert "\033[" in report


def test_report_no_color_no_escape_codes():
    result = ValidationResult(errors=["bad key"])
    report = format_validation_report(result, color=False)
    assert "\033[" not in report


# ---------------------------------------------------------------------------
# validation_summary
# ---------------------------------------------------------------------------

def test_summary_clean():
    result = ValidationResult()
    summary = validation_summary(result, color=False)
    assert "no issues" in summary


def test_summary_counts_errors():
    result = ValidationResult(errors=["e1", "e2"])
    summary = validation_summary(result, color=False)
    assert "2 errors" in summary


def test_summary_singular_error():
    result = ValidationResult(errors=["e1"])
    summary = validation_summary(result, color=False)
    assert "1 error" in summary
    assert "errors" not in summary


def test_summary_counts_warnings():
    result = ValidationResult(warnings=["w1", "w2", "w3"])
    summary = validation_summary(result, color=False)
    assert "3 warnings" in summary


def test_summary_combined():
    result = ValidationResult(errors=["e1"], warnings=["w1", "w2"])
    summary = validation_summary(result, color=False)
    assert "1 error" in summary
    assert "2 warnings" in summary
