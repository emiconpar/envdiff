"""Integration tests combining stringer with parser and diff."""
import pytest
from envdiff.parser import parse_env_string
from envdiff.stringer import to_dotenv, to_inline, to_shell_exports
from envdiff.string_report import format_dotenv_report, stringer_summary


DEV_ENV_TEXT = """
APP_HOST=localhost
APP_PORT=8080
DEBUG=true
DATABASE_URL=postgres://localhost/dev
"""

PROD_ENV_TEXT = """
APP_HOST=prod.example.com
APP_PORT=443
DEBUG=false
DATABASE_URL=postgres://prod-db/app
"""


def test_parse_then_to_dotenv_roundtrip():
    env = parse_env_string(DEV_ENV_TEXT)
    rendered = to_dotenv(env, sort=True)
    re_parsed = parse_env_string(rendered)
    assert re_parsed == env


def test_parse_then_inline_contains_all_keys():
    env = parse_env_string(DEV_ENV_TEXT)
    inline = to_inline(env)
    for key in env:
        assert key in inline


def test_parse_prod_shell_exports_have_export_prefix():
    env = parse_env_string(PROD_ENV_TEXT)
    result = to_shell_exports(env)
    for line in result.splitlines():
        assert line.startswith("export ")


def test_report_integration_shows_all_keys():
    env = parse_env_string(DEV_ENV_TEXT)
    report = format_dotenv_report(env, label="dev", sort=True, color=False)
    for key in env:
        assert key in report


def test_summary_integration_correct_count():
    env = parse_env_string(DEV_ENV_TEXT)
    summary = stringer_summary(env, label="dev")
    assert str(len(env)) in summary


def test_to_dotenv_sorted_matches_expected_order():
    env = parse_env_string(DEV_ENV_TEXT)
    rendered = to_dotenv(env, sort=True)
    keys = [line.split("=")[0] for line in rendered.splitlines() if line]
    assert keys == sorted(keys)
