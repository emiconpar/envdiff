"""Read environment variables from a running process via /proc or psutil."""

import os
from typing import Dict


def get_current_env() -> Dict[str, str]:
    """Return the environment variables of the current process."""
    return dict(os.environ)


def get_process_env(pid: int) -> Dict[str, str]:
    """Read environment variables of a running process by PID.

    On Linux, reads from /proc/<pid>/environ.
    On other platforms, attempts to use psutil if available.

    Args:
        pid: Process ID to inspect.

    Returns:
        Dictionary of environment variable name -> value.

    Raises:
        ProcessLookupError: If the process does not exist or cannot be read.
        RuntimeError: If the platform is unsupported and psutil is unavailable.
    """
    proc_path = f"/proc/{pid}/environ"
    if os.path.exists(proc_path):
        return _read_proc_environ(proc_path)

    # Fallback to psutil
    try:
        import psutil  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "psutil is required to read process environments on this platform. "
            "Install it with: pip install psutil"
        ) from exc

    try:
        proc = psutil.Process(pid)
        return proc.environ()
    except psutil.NoSuchProcess as exc:
        raise ProcessLookupError(f"No process with PID {pid}") from exc
    except psutil.AccessDenied as exc:
        raise PermissionError(
            f"Permission denied reading environment of PID {pid}"
        ) from exc


def _read_proc_environ(path: str) -> Dict[str, str]:
    """Parse /proc/<pid>/environ into a dict."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except PermissionError as exc:
        raise PermissionError(f"Cannot read {path}") from exc
    except FileNotFoundError as exc:
        raise ProcessLookupError(f"Process no longer exists: {path}") from exc

    result: Dict[str, str] = {}
    for entry in data.split(b"\x00"):
        if b"=" in entry:
            key, _, value = entry.partition(b"=")
            result[key.decode(errors="replace")] = value.decode(errors="replace")
    return result
