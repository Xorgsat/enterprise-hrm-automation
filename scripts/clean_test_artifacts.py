#!/usr/bin/env python3
"""
Test Artifacts Cleanup Utility.
Removes stale test logs, screenshots, JUnit XML, and Allure report results.
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TARGET_DIRS = [
    BASE_DIR / "logs",
    BASE_DIR / "reports" / "allure-results",
    BASE_DIR / "reports" / "allure-report",
    BASE_DIR / "reports" / "junit",
    BASE_DIR / "artifacts" / "screenshots",
    BASE_DIR / ".pytest_cache",
]


def clean_artifacts():
    print("Cleaning test automation artifacts...")
    for directory in TARGET_DIRS:
        if directory.exists():
            print(f"Removing: {directory}")
            shutil.rmtree(directory, ignore_errors=True)
            directory.mkdir(parents=True, exist_ok=True)
        else:
            directory.mkdir(parents=True, exist_ok=True)
    print("Artifact cleanup complete.")


if __name__ == "__main__":
    clean_artifacts()
