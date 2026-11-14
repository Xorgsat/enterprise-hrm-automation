"""
Authentication Business Workflow Service.
Orchestrates login, session validation, and logout business processes.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.core.exceptions import WorkflowExecutionException
from hrm_automation.pages.auth.login_page import LoginPage
from hrm_automation.pages.dashboard.dashboard_page import DashboardPage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class AuthenticationWorkflow:
    """Coordinates authentication lifecycles and session boundary validation."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)

    def login_as_admin(self) -> DashboardPage:
        """Perform end-to-end admin login and return validated DashboardPage."""
        logger.info(f"Executing admin login workflow for user '{settings.admin_username}'")
        self.login_page.navigate_to_login()
        self.login_page.login(
            username=settings.admin_username,
            password=settings.admin_password,
        )
        if not self.dashboard_page.is_dashboard_displayed():
            error_msg = ""
            if self.login_page.is_on_login_page():
                try:
                    error_msg = self.login_page.get_alert_error()
                except Exception:
                    pass
            raise WorkflowExecutionException(
                f"Admin login failed. Current URL: '{self.driver.current_url}'. Error message: '{error_msg}'"
            )
        return self.dashboard_page

    def login_expecting_failure(
        self, username: str | None = None, password: str | None = None
    ) -> LoginPage:
        """Submit credentials expecting negative validation or alert."""
        self.login_page.navigate_to_login()
        self.login_page.login(username=username, password=password)
        return self.login_page

    def logout_and_verify(self) -> LoginPage:
        """Perform logout and verify redirection to login view."""
        logger.info("Executing logout workflow.")
        self.dashboard_page.logout()
        if not self.login_page.is_on_login_page():
            raise WorkflowExecutionException(
                f"Logout workflow did not return to login page. Current URL: {self.driver.current_url}"
            )
        return self.login_page
