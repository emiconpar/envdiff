"""Integration tests: parse -> build_side_by_side -> format."""
import pytest
from envdiff.parser import parse_env_string
from envdiff.differ import build_side_by_side
from envdiff.side_by_side_report import format_side_by_side, side_by_side_summary


DEV_ENV = """
APP_HOST=localhost
APP_PORT=8080
DB_URL=postgres://localhost/dev
DEBUG=true
"""

PROD_ENV = """
APP_HOST=prod.example.com
APP_PORT=443
DB_URL=postgres://prod-db/prod
SENTRY_DSN=https://sentry.io/xyz
"""


@pytest.fixture
def dev():
    return parse_env_string(DEV_ENV)


@pytest.fixture
def prod():
    return parse_env_string(PROD_ENV)


def test_parse_then_diff_detects_added(dev, prod):
    diff = build_side_by_side(dev, prod)
    assert any(r.key == "SENTRY_DSN" for r in diff.added())


def test_parse_then_diff_detects_removed(dev, prod):
    diff = build_side_by_side(dev, prod)
    assert any(r.key == "DEBUG" for r in diff.removed())


def test_parse_then_diff_detects_changed_host(dev, prod):
    diff = build_side_by_side(dev, prod)
    changed_keys = [r.key for r in diff.changed()]
    assert "APP_HOST" in changed_keys


def test_parse_then_diff_port_changed(dev, prod):
    diff = build_side_by_side(dev, prod)
    row = next(r for r in diff.changed() if r.key == "APP_PORT")
    assert row.left_value == "8080"
    assert row.right_value == "443"


def test_full_pipeline_format_output(dev, prod):
    diff = build_side_by_side(dev, prod, left_label="dev", right_label="prod")
    output = format_side_by_side(diff, color=False)
    assert "APP_HOST" in output
    assert "dev" in output
    assert "prod" in output


def test_summary_integration(dev, prod):
    diff = build_side_by_side(dev, prod, left_label="dev", right_label="prod")
    summary = side_by_side_summary(diff)
    assert "dev" in summary
    assert "prod" in summary
    # 1 added (SENTRY_DSN), 1 removed (DEBUG), 3 changed
    assert "+1" in summary
    assert "-1" in summary
