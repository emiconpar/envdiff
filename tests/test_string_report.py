"""Tests for envdiff.string_report."""
import pytest
from envdiff.string_report import (
    format_dotenv_report,
    format_inline_report,
    stringer_summary,
)


@pytest.fixture
def env():
    return {"HOST": "localhost", "PORT": "9000", "DEBUG": "true"}


def test_format_dotenv_report_contains_label(env):
    result = format_dotenv_report(env, label="production", color=False)
    assert "production" in result


def test_format_dotenv_report_contains_key_value(env):
    result = format_dotenv_report(env, color=False)
    assert "HOST=localhost" in result


def test_format_dotenv_report_with_export(env):
    result = format_dotenv_report(env, export=True, color=False)
    assert "export HOST=localhost" in result


def test_format_dotenv_report_empty_env():
    result = format_dotenv_report({}, color=False)
    assert "(empty)" in result


def test_format_inline_report_contains_label(env):
    result = format_inline_report(env, label="dev", color=False)
    assert "dev" in result


def test_format_inline_report_contains_key_value(env):
    result = format_inline_report(env, color=False)
    assert "HOST=localhost" in result


def test_format_inline_report_empty_env():
    result = format_inline_report({}, color=False)
    assert "(empty)" in result


def test_format_inline_report_custom_separator(env):
    result = format_inline_report(env, separator=";", sort=True, color=False)
    # body line should use semicolons
    body_line = result.splitlines()[-1]
    assert ";" in body_line


def test_stringer_summary_key_count(env):
    result = stringer_summary(env, label="myenv")
    assert "3" in result
    assert "myenv" in result


def test_stringer_summary_empty():
    result = stringer_summary({}, label="empty")
    assert "0" in result


def test_format_dotenv_report_color_codes_present(env):
    result = format_dotenv_report(env, color=True)
    assert "\033[" in result


def test_format_dotenv_report_no_color_codes(env):
    result = format_dotenv_report(env, color=False)
    assert "\033[" not in result
