"""Tests for envdiff.interpolator."""

import pytest
from envdiff.interpolator import interpolate_value, interpolate_env, find_unresolved


def test_interpolate_value_dollar_brace():
    env = {"HOME": "/home/user"}
    assert interpolate_value("${HOME}/bin", env) == "/home/user/bin"


def test_interpolate_value_dollar_bare():
    env = {"USER": "alice"}
    assert interpolate_value("Hello $USER!", env) == "Hello alice!"


def test_interpolate_value_missing_ref_unchanged():
    env = {}
    assert interpolate_value("${MISSING}", env) == "${MISSING}"


def test_interpolate_value_no_refs():
    assert interpolate_value("plain value", {}) == "plain value"


def test_interpolate_value_multiple_refs():
    env = {"A": "foo", "B": "bar"}
    assert interpolate_value("${A}-${B}", env) == "foo-bar"


def test_interpolate_value_nested():
    env = {"BASE": "/opt", "PATH": "${BASE}/bin"}
    result = interpolate_value("${PATH}/tool", env)
    assert result == "/opt/bin/tool"


def test_interpolate_value_max_depth_prevents_infinite_loop():
    env = {"A": "${A}"}
    result = interpolate_value("${A}", env, max_depth=3)
    assert "${A}" in result


def test_interpolate_env_resolves_all_values():
    env = {"BASE": "/usr", "BIN": "${BASE}/bin"}
    result = interpolate_env(env)
    assert result["BIN"] == "/usr/bin"
    assert result["BASE"] == "/usr"


def test_interpolate_env_uses_context():
    env = {"GREETING": "Hello $NAME"}
    context = {"NAME": "world"}
    result = interpolate_env(env, context=context)
    assert result["GREETING"] == "Hello world"


def test_interpolate_env_returns_new_dict():
    env = {"KEY": "value"}
    result = interpolate_env(env)
    assert result is not env


def test_find_unresolved_detects_missing():
    env = {"PATH": "${UNDEFINED}/bin"}
    unresolved = find_unresolved(env)
    assert "PATH" in unresolved
    assert "UNDEFINED" in unresolved["PATH"]


def test_find_unresolved_empty_when_all_defined():
    env = {"A": "hello", "B": "${A} world"}
    assert find_unresolved(env) == {}


def test_find_unresolved_multiple_missing():
    env = {"X": "${FOO}/${BAR}"}
    unresolved = find_unresolved(env)
    assert set(unresolved["X"]) == {"FOO", "BAR"}


def test_find_unresolved_no_refs_returns_empty():
    env = {"SIMPLE": "no refs here"}
    assert find_unresolved(env) == {}
