"""
Infrastructure and Browser Health Verification Tests.
Validates environment reachability, configuration loading, driver initialization,
and failure capture plumbing.
"""

import pytest
from selenium.webdriver.common.by import By

from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.screenshots import capture_screenshot


@pytest.mark.smoke
class TestInfrastructure:
    """Foundational test suite verifying automation harness integrity."""

    def test_configuration_loading(self, env_settings):
        """Verify configuration loads correctly from environment and YAML."""
        assert env_settings.base_url.startswith("http")
        assert env_settings.admin_username == "Admin"
        assert env_settings.default_timeout > 0
        assert env_settings.browser == "chrome"

    def test_browser_lifecycle_and_navigation(self, driver, env_settings):
        """Verify WebDriver initializes, navigates to base URL, and reads DOM title."""
        base_page = BasePage(driver)
        login_url = f"{env_settings.base_url}/web/index.php/auth/login"
        base_page.open_url(login_url)

        assert "orangehrm" in base_page.current_url.lower()
        assert "OrangeHRM" in base_page.title

        # Verify username input is visible via BasePage find
        username_elem = base_page.find((By.NAME, "username"))
        assert username_elem.is_displayed()

    def test_screenshot_capture_utility(self, driver, env_settings):
        """Verify diagnostic screenshot capture successfully writes to disk."""
        base_page = BasePage(driver)
        base_page.open_url(f"{env_settings.base_url}/web/index.php/auth/login")

        path = capture_screenshot(driver, name="test_infra_screenshot", attach_to_allure=False)
        assert path is not None
        assert path.exists()
        assert path.stat().st_size > 0
