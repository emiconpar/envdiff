"""Integration tests combining interpolator with parser and report."""

from envdiff.interpolator import interpolate_env, find_unresolved
from envdiff.interpolation_report import format_interpolation_report, interpolation_summary
from envdiff.parser import parse_env_string


RAW_ENV = """
BASE_DIR=/opt/myapp
LOG_DIR=${BASE_DIR}/logs
DATA_DIR=${BASE_DIR}/data
DATABASE_URL=postgres://localhost/${DB_NAME}
APP_ENV=production
"""


def test_parse_then_interpolate_resolves_base_dir():
    env = parse_env_string(RAW_ENV)
    result = interpolate_env(env)
    assert result["LOG_DIR"] == "/opt/myapp/logs"
    assert result["DATA_DIR"] == "/opt/myapp/data"


def test_parse_then_interpolate_leaves_missing_unresolved():
    env = parse_env_string(RAW_ENV)
    result = interpolate_env(env)
    assert "${DB_NAME}" in result["DATABASE_URL"]


def test_find_unresolved_after_parse():
    env = parse_env_string(RAW_ENV)
    unresolved = find_unresolved(env)
    assert "DATABASE_URL" in unresolved
    assert "DB_NAME" in unresolved["DATABASE_URL"]


def test_report_integration_shows_resolved_and_unresolved():
    env = parse_env_string(RAW_ENV)
    interpolated = interpolate_env(env)
    unresolved = find_unresolved(env)
    report = format_interpolation_report(
        env, interpolated, unresolved, label="test", color=False
    )
    assert "LOG_DIR" in report
    assert "DB_NAME" in report
    assert "test" in report


def test_summary_integration_reports_unresolved_count():
    env = parse_env_string(RAW_ENV)
    unresolved = find_unresolved(env)
    summary = interpolation_summary(unresolved, color=False)
    assert "unresolved" in summary.lower()


def test_no_unresolved_when_all_defined():
    raw = "BASE=/usr\nBIN=${BASE}/bin\nSBIN=${BASE}/sbin\n"
    env = parse_env_string(raw)
    unresolved = find_unresolved(env)
    assert unresolved == {}


def test_interpolate_with_external_context():
    env = parse_env_string("GREETING=Hello $NAME")
    result = interpolate_env(env, context={"NAME": "envdiff"})
    assert result["GREETING"] == "Hello envdiff"
