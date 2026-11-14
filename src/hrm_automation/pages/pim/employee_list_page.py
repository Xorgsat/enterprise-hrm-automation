"""
Page Object for OrangeHRM PIM Employee List Screen.
Encapsulates search filters, data table grid, and Add Employee navigation.
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


class EmployeeListPage(BasePage):
    """Encapsulates /web/index.php/pim/viewEmployeeList."""

    # Action Buttons
    ADD_BUTTON = (By.XPATH, "//button[normalize-space(.)='Add' or contains(.,'Add')]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space(.)='Reset']")

    # Search Filter Inputs
    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Employee Name']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    EMPLOYEE_ID_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    RECORDS_COUNT_LABEL = (By.CSS_SELECTOR, ".orangehrm-horizontal-padding .oxd-text--span")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.sidebar = SidebarComponent(driver)
        self.table = DataTableComponent(driver)
        self.dropdown = DropdownComponent(driver)
        self.list_url = f"{settings.base_url}/web/index.php/pim/viewEmployeeList"

    def navigate_to_list(self) -> "EmployeeListPage":
        """Navigate to PIM Employee List page."""
        logger.info(f"Navigating to PIM employee list: {self.list_url}")
        self.open_url(self.list_url)
        self.wait.wait_for_visibility(self.ADD_BUTTON)
        self.wait.wait_for_visibility(self.table.TABLE_CONTAINER)
        self.wait_for_page_readiness()
        return self

    def click_add_employee(self) -> None:
        """Click the top 'Add' button to navigate to Add Employee form."""
        logger.info("Clicking 'Add' button to create new employee.")
        self.click(self.ADD_BUTTON)
        self.wait.wait_for_url_contains("/pim/addEmployee")

    def search_by_id(self, employee_id: str) -> None:
        """Filter employees by exact Employee ID."""
        logger.info(f"Searching employee list by ID: '{employee_id}'")
        self.type_text(self.EMPLOYEE_ID_INPUT, employee_id, clear_first=True)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()

    def search_by_name(self, employee_name: str) -> None:
        """Filter employees by name prefix."""
        logger.info(f"Searching employee list by Name: '{employee_name}'")
        self.type_text(self.EMPLOYEE_NAME_INPUT, employee_name, clear_first=True)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()

    def reset_search(self) -> None:
        """Clear all search filter criteria."""
        logger.debug("Resetting employee search filters.")
        self.click(self.RESET_BUTTON)
        self.wait_for_page_readiness()

    def is_employee_present_in_table(self, identifier: str) -> bool:
        """Check if any row in the table contains the given identifier (name or ID)."""
        return self.table.find_row_index_by_text(identifier) is not None

    def get_records_count_text(self) -> str:
        """Retrieve the records found summary text (e.g. '(1) Record Found')."""
        if self.is_visible(self.RECORDS_COUNT_LABEL, timeout=3):
            return self.get_text(self.RECORDS_COUNT_LABEL)
        return ""
