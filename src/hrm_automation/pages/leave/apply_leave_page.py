"""
Page Object for OrangeHRM Apply Leave Screen.
Encapsulates /web/index.php/leave/applyLeave.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.components.dropdown import DropdownComponent
from hrm_automation.components.toast import ToastComponent
from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class ApplyLeavePage(BasePage):
    """Encapsulates employee leave application form."""

    LEAVE_TYPE_WRAPPER = (
        By.XPATH,
        "//label[normalize-space(text())='Leave Type']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text')]",
    )
    FROM_DATE_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='From Date']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    TO_DATE_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='To Date']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    COMMENTS_TEXTAREA = (
        By.XPATH,
        "//label[normalize-space(text())='Comments']/ancestor::div[contains(@class,'oxd-input-group')]//textarea",
    )
    APPLY_BUTTON = (By.XPATH, "//button[normalize-space(.)='Apply' or @type='submit']")
    INPUT_ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-group__message")
    NO_BALANCE_MESSAGE = (
        By.XPATH,
        "//p[contains(., 'No Leave Types with Leave Balance')] | //*[contains(@class, 'oxd-text') and contains(., 'No Leave Types')]",
    )
    PAGE_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.dropdown = DropdownComponent(driver)
        self.toast = ToastComponent(driver)
        self.apply_url = f"{settings.base_url}/web/index.php/leave/applyLeave"

    def navigate_to_apply(self) -> "ApplyLeavePage":
        """Navigate directly to the Apply Leave form."""
        logger.info(f"Navigating to Apply Leave: {self.apply_url}")
        self.open_url(self.apply_url)
        self.wait.wait_for_visibility(self.PAGE_HEADER)
        self.wait_for_page_readiness()
        return self

    def has_no_leave_balance_warning(self) -> bool:
        """Check if 'No Leave Types with Leave Balance' warning is displayed."""
        return self.is_visible(self.NO_BALANCE_MESSAGE, timeout=3)

    def click_apply(self) -> None:
        """Submit the leave application form."""
        logger.info("Submitting leave application.")
        self.click(self.APPLY_BUTTON)

    def get_field_errors(self) -> list[str]:
        """Retrieve all currently visible inline form error messages."""
        elements = self.find_all(self.INPUT_ERROR_MESSAGES)
        return [e.text.strip() for e in elements if e.text.strip()]
