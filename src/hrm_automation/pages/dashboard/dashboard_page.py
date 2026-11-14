"""
Page Object for OrangeHRM Dashboard Screen.
Encapsulates dashboard landing validation, user profile dropdown, and logout trigger.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.components.sidebar import SidebarComponent
from hrm_automation.components.toast import ToastComponent
from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class DashboardPage(BasePage):
    """Encapsulates the /web/index.php/dashboard/index interface."""

    HEADER_TITLE = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    USER_NAME_LABEL = (By.CSS_SELECTOR, ".oxd-userdropdown-name")
    LOGOUT_LINK = (
        By.XPATH,
        "//ul[contains(@class,'oxd-dropdown-menu')]//a[normalize-space(text())='Logout']",
    )
    DASHBOARD_GRID = (By.CSS_SELECTOR, ".orangehrm-dashboard-grid")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.sidebar = SidebarComponent(driver)
        self.toast = ToastComponent(driver)

    def is_dashboard_displayed(self, timeout: int = 10) -> bool:
        """Verify navigation to dashboard URL and header presence."""
        try:
            self.wait.wait_for_url_contains("/dashboard/index", timeout=timeout)
            return self.is_visible(self.HEADER_TITLE, timeout=timeout)
        except Exception:
            return False

    def verify_is_displayed(self, timeout: int = 10) -> "DashboardPage":
        """Assert dashboard readiness and return self."""
        self.wait.wait_for_url_contains("/dashboard/index", timeout=timeout)
        self.wait.wait_for_visibility(self.HEADER_TITLE, timeout=timeout)
        return self

    def get_logged_in_user_name(self) -> str:
        """Retrieve the name displayed on the user avatar dropdown."""
        return self.get_text(self.USER_NAME_LABEL)

    def logout(self) -> None:
        """Click user avatar dropdown and trigger Logout."""
        logger.info("Logging out of current session.")
        self.click(self.USER_DROPDOWN)
        self.wait.wait_for_visibility(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK)
        self.wait.wait_for_url_contains("/auth/login")
        self.wait_for_page_readiness()
