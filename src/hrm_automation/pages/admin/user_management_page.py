"""
Page Object for OrangeHRM Admin User Management Screen.
Encapsulates /web/index.php/admin/viewSystemUsers.
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


class UserManagementPage(BasePage):
    """Encapsulates the /web/index.php/admin/viewSystemUsers interface."""

    ADD_BUTTON = (By.XPATH, "//button[normalize-space(.)='Add' or contains(.,'Add')]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space(.)='Reset']")

    USERNAME_FILTER_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Username']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    RECORDS_COUNT_LABEL = (By.CSS_SELECTOR, ".orangehrm-horizontal-padding .oxd-text--span")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.sidebar = SidebarComponent(driver)
        self.table = DataTableComponent(driver)
        self.dropdown = DropdownComponent(driver)
        self.url = f"{settings.base_url}/web/index.php/admin/viewSystemUsers"

    def navigate_to_user_management(self) -> "UserManagementPage":
        """Navigate directly to User Management view."""
        logger.info(f"Navigating to User Management: {self.url}")
        self.open_url(self.url)
        self.wait.wait_for_visibility(self.ADD_BUTTON)
        self.wait_for_page_readiness()
        return self

    def click_add_user(self) -> None:
        """Click the Add button to open Add User form."""
        logger.info("Clicking Add button to provision new system user.")
        self.click(self.ADD_BUTTON)
        self.wait.wait_for_url_contains("/admin/saveSystemUser")

    def search_by_username(self, username: str) -> None:
        """Filter system users by exact username."""
        logger.info(f"Filtering users by username: '{username}'")
        self.type_text(self.USERNAME_FILTER_INPUT, username, clear_first=True)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()

    def filter_by_role(self, role: str) -> None:
        """Filter system users by User Role ('Admin' or 'ESS')."""
        logger.info(f"Filtering users by role: '{role}'")
        self.dropdown.select_by_label_and_text("User Role", role)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()

    def filter_by_status(self, status: str) -> None:
        """Filter system users by Status ('Enabled' or 'Disabled')."""
        logger.info(f"Filtering users by status: '{status}'")
        self.dropdown.select_by_label_and_text("Status", status)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()

    def reset_filters(self) -> None:
        """Clear search filter parameters."""
        self.click(self.RESET_BUTTON)
        self.wait_for_page_readiness()

    def is_user_present_in_table(self, username: str) -> bool:
        """Check if any row in the users table contains the username."""
        return self.table.find_row_index_by_text(username) is not None

    def get_records_count_text(self) -> str:
        """Retrieve the records found summary text."""
        if self.is_visible(self.RECORDS_COUNT_LABEL, timeout=3):
            return self.get_text(self.RECORDS_COUNT_LABEL)
        return ""
