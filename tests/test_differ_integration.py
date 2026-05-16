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


@pytest.fixture
def diff(dev, prod):
    """Pre-built side-by-side diff used by multiple tests."""
    return build_side_by_side(dev, prod, left_label="dev", right_label="prod")


def test_parse_then_diff_detects_added(diff):
    assert any(r.key == "SENTRY_DSN" for r in diff.added())


def test_parse_then_diff_detects_removed(diff):
    assert any(r.key == "DEBUG" for r in diff.removed())


def test_parse_then_diff_detects_changed_host(diff):
    changed_keys = [r.key for r in diff.changed()]
    assert "APP_HOST" in changed_keys


def test_parse_then_diff_port_changed(diff):
    row = next(r for r in diff.changed() if r.key == "APP_PORT")
    assert row.left_value == "8080"
    assert row.right_value == "443"


def test_full_pipeline_format_output(diff):
    output = format_side_by_side(diff, color=False)
    assert "APP_HOST" in output
    assert "dev" in output
    assert "prod" in output


def test_summary_integration(diff):
    summary = side_by_side_summary(diff)
    assert "dev" in summary
    assert "prod" in summary
    # 1 added (SENTRY_DSN), 1 removed (DEBUG), 3 changed
    assert "+1" in summary
    assert "-1" in summary


def test_unchanged_keys_not_in_changed_or_added_or_removed(diff):
    """Keys present with the same value in both envs must not appear in any diff bucket."""
    all_diff_keys = (
        {r.key for r in diff.added()}
        | {r.key for r in diff.removed()}
        | {r.key for r in diff.changed()}
    )
    # DB_URL differs, so only keys that are truly identical should be absent
    for row in diff.unchanged():
        assert row.key not in all_diff_keys, (
            f"{row.key!r} appears in both unchanged and a diff bucket"
        )
