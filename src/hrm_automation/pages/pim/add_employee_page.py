"""
Page Object for OrangeHRM Add Employee Screen.
Encapsulates employee identity creation, login details toggle, and validation messages.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.core.base_page import BasePage
from hrm_automation.data.models.employee import EmployeeData
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class AddEmployeePage(BasePage):
    """Encapsulates /web/index.php/pim/addEmployee."""

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMPLOYEE_ID_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    CREATE_LOGIN_SWITCH = (By.CSS_SELECTOR, ".oxd-switch-input")
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space(.)='Save' or @type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(.)='Cancel']")
    INPUT_ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-group__message")

    # Dynamic fields when 'Create Login Details' is active
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

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.add_url = f"{settings.base_url}/web/index.php/pim/addEmployee"

    def navigate_to_add_employee(self) -> "AddEmployeePage":
        """Directly navigate to Add Employee view."""
        self.open_url(self.add_url)
        self.wait.wait_for_visibility(self.FIRST_NAME_INPUT)
        return self

    def enter_employee_details(self, employee: EmployeeData) -> "AddEmployeePage":
        """Populate identity fields from an EmployeeData instance."""
        logger.info(f"Populating employee form for: {employee.full_name}")
        self.type_text(self.FIRST_NAME_INPUT, employee.first_name)
        if employee.middle_name:
            self.type_text(self.MIDDLE_NAME_INPUT, employee.middle_name)
        self.type_text(self.LAST_NAME_INPUT, employee.last_name)

        if employee.employee_id:
            self.type_text(self.EMPLOYEE_ID_INPUT, employee.employee_id, clear_first=True)
            # Sync the actual value captured in the form
            employee.employee_id = self.get_assigned_employee_id()

        if employee.username and employee.password:
            self.enable_login_details(employee.username, employee.password)

        return self

    def get_assigned_employee_id(self) -> str:
        """Read the currently populated value in the Employee ID input."""
        return self.get_attribute(self.EMPLOYEE_ID_INPUT, "value") or ""

    def enable_login_details(self, username: str, password: str) -> None:
        """Toggle the login credentials switch and enter username/password."""
        logger.debug(f"Enabling login credentials for user: '{username}'")
        self.click(self.CREATE_LOGIN_SWITCH)
        self.wait.wait_for_visibility(self.USERNAME_INPUT)
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.CONFIRM_PASSWORD_INPUT, password)

    def click_save(self) -> None:
        """Submit the Add Employee form."""
        logger.info("Submitting Add Employee form.")
        self.click(self.SAVE_BUTTON)

    def click_cancel(self) -> None:
        """Click Cancel to abort creation."""
        logger.info("Canceling Add Employee form.")
        self.click(self.CANCEL_BUTTON)
        self.wait.wait_for_url_contains("/pim/viewEmployeeList")

    def get_field_errors(self) -> list[str]:
        """Retrieve visible validation error texts."""
        elements = self.find_all(self.INPUT_ERROR_MESSAGES)
        return [e.text.strip() for e in elements if e.text.strip()]
