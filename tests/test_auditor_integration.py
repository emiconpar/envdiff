"""Integration tests combining parser, auditor, and audit_report."""

from envdiff.parser import parse_env_string
from envdiff.auditor import audit_env
from envdiff.audit_report import format_audit_report, audit_summary


ENV_CONTENT_CLEAN = """
APP_ENV=development
LOG_LEVEL=info
PORT=8080
"""

ENV_CONTENT_SECRETS = """
APP_ENV=production
LOG_LEVEL=warn
AWS_SECRET_ACCESS_KEY=realkey123
DB_PASSWORD=supersecret
EMPTY_VAR=
"""


def test_parse_then_audit_clean_passes():
    env = parse_env_string(ENV_CONTENT_CLEAN)
    result = audit_env(env, label="clean")
    assert result.passed


def test_parse_then_audit_detects_forbidden():
    env = parse_env_string(ENV_CONTENT_SECRETS)
    result = audit_env(env)
    assert "AWS_SECRET_ACCESS_KEY" in result.forbidden_found


def test_parse_then_audit_detects_plain_secret():
    env = parse_env_string(ENV_CONTENT_SECRETS)
    result = audit_env(env)
    assert "DB_PASSWORD" in result.plain_secrets


def test_parse_then_audit_production_empty_warning():
    env = parse_env_string(ENV_CONTENT_SECRETS)
    result = audit_env(env)
    assert any("EMPTY_VAR" in w for w in result.warnings)


def test_full_pipeline_report_contains_key():
    env = parse_env_string(ENV_CONTENT_SECRETS)
    result = audit_env(env, label="prod")
    report = format_audit_report(result, color=False)
    assert "AWS_SECRET_ACCESS_KEY" in report
    assert "prod" in report


def test_full_pipeline_summary_reflects_failures():
    env = parse_env_string(ENV_CONTENT_SECRETS)
    result = audit_env(env, label="prod")
    summary = audit_summary(result)
    assert "FAILED" in summary
