#!/usr/bin/env python3
"""
Full Regression Test Runner Script.
Supports parallel execution across workers with comprehensive reporting.
"""

import argparse
import subprocess
import sys


def run_regression():
    parser = argparse.ArgumentParser(description="Run HRM Test Suite")
    parser.add_argument("-n", "--workers", default="2", help="Number of parallel pytest workers")
    parser.add_argument("-m", "--marker", default=None, help="Pytest marker filter")
    args = parser.parse_args()

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-n",
        str(args.workers),
        "-v",
        "--junitxml=reports/junit/regression-results.xml",
        "--alluredir=reports/allure-results",
    ]
    if args.marker:
        cmd.extend(["-m", args.marker])

    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_regression()
