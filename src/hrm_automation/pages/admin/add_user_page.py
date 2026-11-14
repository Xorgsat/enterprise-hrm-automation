"""
Page Object for OrangeHRM Add System User Screen.
Encapsulates /web/index.php/admin/saveSystemUser.
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.components.dropdown import DropdownComponent
from hrm_automation.components.toast import ToastComponent
from hrm_automation.core.base_page import BasePage
from hrm_automation.data.models.user import SystemUserData
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class AddUserPage(BasePage):
    """Encapsulates provisioning a system user account."""

    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Employee Name']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    AUTOCOMPLETE_DROPDOWN = (By.CSS_SELECTOR, ".oxd-autocomplete-dropdown")
    AUTOCOMPLETE_OPTION = (By.CSS_SELECTOR, ".oxd-autocomplete-option")

    USERNAME_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Username']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    PASSWORD_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Password']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    CONFIRM_PASSWORD_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Confirm Password']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space(.)='Save' or @type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(.)='Cancel']")
    INPUT_ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-group__message")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.dropdown = DropdownComponent(driver)
        self.toast = ToastComponent(driver)
        self.add_url = f"{settings.base_url}/web/index.php/admin/saveSystemUser"

    def navigate_to_add_user(self) -> "AddUserPage":
        """Navigate directly to the Add User page."""
        self.open_url(self.add_url)
        self.wait.wait_for_visibility(self.USERNAME_INPUT)
        return self

    def enter_user_details(self, user: SystemUserData) -> "AddUserPage":
        """Fill out system user provisioning form."""
        logger.info(
            f"Provisioning system user '{user.username}' for employee '{user.employee_name}'"
        )

        # Select Role
        self.dropdown.select_by_label_and_text("User Role", user.user_role)

        # Autocomplete employee name
        self.type_text(self.EMPLOYEE_NAME_INPUT, user.employee_name)
        self.wait.wait_for_visibility(self.AUTOCOMPLETE_DROPDOWN, timeout=6)
        time.sleep(0.3)
        self.click(self.AUTOCOMPLETE_OPTION)

        # Select Status
        self.dropdown.select_by_label_and_text("Status", user.status)

        # Credentials
        self.type_text(self.USERNAME_INPUT, user.username)
        self.type_text(self.PASSWORD_INPUT, user.password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, user.confirm_password or user.password)

        return self

    def click_save(self) -> None:
        """Submit the Add User form."""
        logger.info("Submitting Add User form.")
        self.click(self.SAVE_BUTTON)
        self.wait_for_page_readiness()

    def click_cancel(self) -> None:
        """Cancel user creation."""
        self.click(self.CANCEL_BUTTON)
        self.wait.wait_for_url_contains("/admin/viewSystemUsers")

    def get_field_errors(self, timeout: int = 5) -> list[str]:
        """Retrieve all currently visible inline form error messages with synchronization."""
        try:
            self.wait.wait_for_presence(self.INPUT_ERROR_MESSAGES, timeout=timeout)
        except Exception:
            pass
        time.sleep(0.5)
        elements = self.find_all(self.INPUT_ERROR_MESSAGES)
        return [e.text.strip() for e in elements if e.text.strip()]
