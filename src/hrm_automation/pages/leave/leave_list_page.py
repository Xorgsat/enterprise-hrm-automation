"""
Page Object for OrangeHRM Leave List Screen.
Encapsulates /web/index.php/leave/viewLeaveList.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.components.data_table import DataTableComponent
from hrm_automation.components.dropdown import DropdownComponent
from hrm_automation.components.sidebar import SidebarComponent
from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class LeaveListPage(BasePage):
    """Encapsulates viewing and managing submitted leave requests."""

    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space(.)='Reset']")
    APPLY_NAV_TAB = (
        By.XPATH,
        "//nav[contains(@class,'oxd-topbar-body-nav')]//a[normalize-space(text())='Apply']",
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.sidebar = SidebarComponent(driver)
        self.table = DataTableComponent(driver)
        self.dropdown = DropdownComponent(driver)
        self.list_url = f"{settings.base_url}/web/index.php/leave/viewLeaveList"

    def navigate_to_leave_list(self) -> "LeaveListPage":
        """Navigate to the Leave List view."""
        logger.info(f"Navigating to Leave List: {self.list_url}")
        self.open_url(self.list_url)
        self.wait.wait_for_visibility(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()
        return self

    def navigate_to_apply_leave(self) -> None:
        """Click top sub-tab 'Apply' to navigate to Leave Application form."""
        logger.info("Navigating to Apply Leave tab.")
        self.click(self.APPLY_NAV_TAB)
        self.wait.wait_for_url_contains("/leave/applyLeave")
