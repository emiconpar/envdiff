"""Tests for envdiff.audit_report."""

import pytest
from envdiff.auditor import AuditResult
from envdiff.audit_report import format_audit_report, audit_summary


@pytest.fixture
def clean_result():
    return AuditResult(label="clean-env")


@pytest.fixture
def dirty_result():
    return AuditResult(
        label="dirty-env",
        forbidden_found=["AWS_SECRET_KEY"],
        missing_required=["LOG_LEVEL"],
        plain_secrets=["DB_PASSWORD"],
        warnings=["Empty value for 'PORT' in production"],
    )


def test_report_shows_label(clean_result):
    report = format_audit_report(clean_result, color=False)
    assert "clean-env" in report


def test_report_passed_message(clean_result):
    report = format_audit_report(clean_result, color=False)
    assert "PASSED" in report


def test_report_failed_message(dirty_result):
    report = format_audit_report(dirty_result, color=False)
    assert "FAILED" in report


def test_report_shows_forbidden_key(dirty_result):
    report = format_audit_report(dirty_result, color=False)
    assert "AWS_SECRET_KEY" in report


def test_report_shows_missing_required(dirty_result):
    report = format_audit_report(dirty_result, color=False)
    assert "LOG_LEVEL" in report


def test_report_shows_plain_secret(dirty_result):
    report = format_audit_report(dirty_result, color=False)
    assert "DB_PASSWORD" in report


def test_report_shows_warning(dirty_result):
    report = format_audit_report(dirty_result, color=False)
    assert "PORT" in report


def test_summary_passed(clean_result):
    summary = audit_summary(clean_result)
    assert "PASSED" in summary
    assert "clean-env" in summary


def test_summary_failed(dirty_result):
    summary = audit_summary(dirty_result)
    assert "FAILED" in summary


def test_summary_issue_count(dirty_result):
    summary = audit_summary(dirty_result)
    # 3 issues: 1 forbidden + 1 missing + 1 plain secret
    assert "3 issue(s)" in summary


def test_summary_warning_count(dirty_result):
    summary = audit_summary(dirty_result)
    assert "1 warning(s)" in summary
