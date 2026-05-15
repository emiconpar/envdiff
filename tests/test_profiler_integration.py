"""Integration tests for profiler + profile_report + parser."""

from envdiff.parser import parse_env_string
from envdiff.profiler import profile_env, compare_profiles
from envdiff.profile_report import format_profile_report, format_comparison_report, profile_summary


ENV_A = """
APP_HOST=localhost
APP_PORT=8080
APP_SECRET=
DB_URL=postgres://localhost/dev
"""

ENV_B = """
APP_HOST=prod.example.com
APP_PORT=443
APP_SECRET=supersecret
DB_URL=postgres://prod/main
DB_POOL=10
FEATURE_FLAG=true
"""


def test_parse_then_profile_key_count():
    env = parse_env_string(ENV_A)
    profile = profile_env(env, label="dev")
    assert profile.total_keys == 4


def test_parse_then_profile_detects_empty():
    env = parse_env_string(ENV_A)
    profile = profile_env(env, label="dev")
    assert "APP_SECRET" in profile.empty_values


def test_parse_then_profile_prefix_grouping():
    env = parse_env_string(ENV_B)
    profile = profile_env(env, label="prod")
    assert profile.prefixes.get("APP") == 3
    assert profile.prefixes.get("DB") == 2


def test_compare_two_parsed_envs():
    env_a = parse_env_string(ENV_A)
    env_b = parse_env_string(ENV_B)
    pa = profile_env(env_a, label="dev")
    pb = profile_env(env_b, label="prod")
    cmp = compare_profiles(pa, pb)
    assert cmp["total_keys"]["dev"] == 4
    assert cmp["total_keys"]["prod"] == 6


def test_format_report_integration():
    env = parse_env_string(ENV_B)
    profile = profile_env(env, label="prod")
    report = format_profile_report(profile, color=False)
    assert "prod" in report
    assert "6" in report


def test_comparison_report_integration():
    env_a = parse_env_string(ENV_A)
    env_b = parse_env_string(ENV_B)
    pa = profile_env(env_a, label="dev")
    pb = profile_env(env_b, label="prod")
    report = format_comparison_report(pa, pb, color=False)
    assert "dev" in report
    assert "prod" in report


def test_summary_integration():
    env = parse_env_string(ENV_A)
    profile = profile_env(env, label="dev")
    summary = profile_summary(profile)
    assert "dev" in summary
    assert "keys" in summary
