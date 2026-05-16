"""Integration tests: masker + parser + mask_report."""

from envdiff.parser import parse_env_string
from envdiff.masker import mask_env, mask_summary
from envdiff.mask_report import format_mask_report, masking_summary
from envdiff.redactor import _is_sensitive


RAW_ENV = """
APP_NAME=myapp
DB_PASSWORD=hunter2
API_KEY=abc123secret
DEBUG=false
SECRET_TOKEN=tok_live_xyz
"""


def test_parse_then_mask_sensitive_keys():
    env = parse_env_string(RAW_ENV)
    sensitive = {k for k in env if _is_sensitive(k)}
    masked = mask_env(env, sensitive)
    for key in sensitive:
        assert masked[key] == "***"
    assert masked["APP_NAME"] == "myapp"
    assert masked["DEBUG"] == "false"


def test_mask_summary_after_parse():
    env = parse_env_string(RAW_ENV)
    sensitive = {k for k in env if _is_sensitive(k)}
    masked = mask_env(env, sensitive)
    summary = mask_summary(masked, env)
    assert summary["masked_count"] == len(sensitive)
    assert summary["total_keys"] == len(env)


def test_report_integration_shows_all_masked_keys():
    env = parse_env_string(RAW_ENV)
    sensitive = {k for k in env if _is_sensitive(k)}
    masked = mask_env(env, sensitive)
    report = format_mask_report(masked, env, label="test", color=False)
    for key in sensitive:
        assert key in report


def test_partial_mask_integration_reveals_suffix():
    env = parse_env_string(RAW_ENV)
    sensitive = {k for k in env if _is_sensitive(k)}
    masked = mask_env(env, sensitive, partial=True, reveal_chars=4)
    for key in sensitive:
        original_val = env[key]
        if len(original_val) > 4:
            assert masked[key].endswith(original_val[-4:])


def test_summary_line_integration():
    env = parse_env_string(RAW_ENV)
    sensitive = {k for k in env if _is_sensitive(k)}
    masked = mask_env(env, sensitive)
    line = masking_summary(masked, env)
    assert "masked" in line
    assert str(len(sensitive)) in line
