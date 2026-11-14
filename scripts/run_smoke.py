#!/usr/bin/env python3
"""
Smoke Test Runner Script.
Executes business-critical smoke verification suite with reporting flags.
"""

import subprocess
import sys


def run_smoke():
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-m",
        "smoke",
        "-v",
        "--junitxml=reports/junit/smoke-results.xml",
        "--alluredir=reports/allure-results",
    ]
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_smoke()
