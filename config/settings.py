"""
Central Configuration Management for Enterprise HRM Automation Framework.
Handles environment configuration, browser settings, credentials, and timeouts.
"""

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
ENVIRONMENTS_DIR = CONFIG_DIR / "environments"


class FrameworkSettings(BaseSettings):
    """Framework runtime settings loaded from environment variables and environment YAML."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Core environment target
    environment: str = Field(default="demo", alias="ENVIRONMENT")
    base_url: str = Field(default="https://opensource-demo.orangehrmlive.com", alias="BASE_URL")

    # Credentials
    admin_username: str = Field(default="Admin", alias="ADMIN_USERNAME")
    admin_password: str = Field(default="admin123", alias="ADMIN_PASSWORD")
    employee_username: str | None = Field(default=None, alias="EMPLOYEE_USERNAME")
    employee_password: str | None = Field(default=None, alias="EMPLOYEE_PASSWORD")

    # Browser Execution
    browser: str = Field(default="chrome", alias="BROWSER")
    headless: bool = Field(default=True, alias="HEADLESS")
    window_width: int = Field(default=1920, alias="WINDOW_WIDTH")
    window_height: int = Field(default=1080, alias="WINDOW_HEIGHT")

    # Timeouts & Synchronization
    default_timeout: int = Field(default=15, alias="DEFAULT_TIMEOUT")
    page_load_timeout: int = Field(default=60, alias="PAGE_LOAD_TIMEOUT")
    implicit_wait: int = Field(default=0, alias="IMPLICIT_WAIT")

    # Concurrency & Reporting
    workers: int = Field(default=2, alias="WORKERS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    screenshot_on_failure: bool = Field(default=True, alias="SCREENSHOT_ON_FAILURE")
    save_allure_results: bool = Field(default=True, alias="SAVE_ALLURE_RESULTS")

    # Environment-specific metadata loaded from YAML
    env_metadata: dict[str, Any] = Field(default_factory=dict)

    def load_environment_yaml(self) -> None:
        """Load additional environment configuration from YAML if present."""
        env_file = ENVIRONMENTS_DIR / f"{self.environment}.yaml"
        if env_file.exists():
            with open(env_file, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                self.env_metadata = data
                if "base_url" in data and not os.getenv("BASE_URL"):
                    self.base_url = data["base_url"]
                if "default_timeout" in data and not os.getenv("DEFAULT_TIMEOUT"):
                    self.default_timeout = data["default_timeout"]
                if "page_load_timeout" in data and not os.getenv("PAGE_LOAD_TIMEOUT"):
                    self.page_load_timeout = data["page_load_timeout"]


# Singleton instance
settings = FrameworkSettings()
settings.load_environment_yaml()
