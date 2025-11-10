# tests/conftest.py

# Ensure repo root is importable (so `tools` works)
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import os, time
import pytest
from tools.audit_log import append_run_summary


def pytest_addoption(parser):
    parser.addoption("--pqi-cycle", action="store", default=os.getenv("PQI_CYCLE", "I"))
    parser.addoption("--pqi-version", action="store", default=os.getenv("PQI_VERSION", "v0.2"))
    parser.addoption("--pqi-notes", action="store", default=os.getenv("PQI_NOTES", ""))
    parser.addoption(
        "--pqi-autolog",
        action="store_true",
        default=os.getenv("PQI_AUTOLOG", "0") == "1",
    )


def pytest_sessionstart(session):
    # Use config as a safe shared store
    session.config._pqi_start_time = time.time()
    session.config._pqi_counts = {"tests": 0, "passed": 0, "failed": 0, "skipped": 0}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Use hookwrapper so we can inspect the finished report (rep).
    Update counts only on the 'call' phase.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    counts = item.session.config._pqi_counts
    counts["tests"] += 1
    if rep.passed:
        counts["passed"] += 1
    elif rep.failed:
        counts["failed"] += 1
    elif rep.skipped:
        counts["skipped"] += 1


def pytest_sessionfinish(session, exitstatus):
    if not session.config.getoption("--pqi-autolog"):
        return

    counts = session.config._pqi_counts
    duration = time.time() - session.config._pqi_start_time
    append_run_summary(
        version=session.config.getoption("--pqi-version"),
        test_cycle=session.config.getoption("--pqi-cycle"),
        tests=counts["tests"],
        passed=counts["passed"],
        failed=counts["failed"],
        skipped=counts["skipped"],
        duration_s=duration,
        notes=session.config.getoption("--pqi-notes") or f"exit={exitstatus}",
    )
