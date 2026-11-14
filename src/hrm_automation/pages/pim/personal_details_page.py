"""
Page Object for OrangeHRM Employee Personal Details Screen.
Encapsulates /web/index.php/pim/viewPersonalDetails/empNumber/{id}.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.components.dropdown import DropdownComponent
from hrm_automation.components.toast import ToastComponent
from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class PersonalDetailsPage(BasePage):
    """Encapsulates viewing and modifying an employee's personal record."""

    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")
    NICKNAME = (
        By.XPATH,
        "//label[normalize-space(text())='Nickname']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    OTHER_ID = (
        By.XPATH,
        "//label[normalize-space(text())='Other Id']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    DRIVER_LICENSE = (
        By.XPATH,
        "//label[normalize-space(text())=\"Driver's License Number\"]/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'orangehrm-horizontal-padding')]//button[normalize-space(.)='Save'][1]",
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.toast = ToastComponent(driver)
        self.dropdown = DropdownComponent(driver)

    def is_loaded(self, timeout: int = 15) -> bool:
        """Verify the personal details view has loaded."""
        try:
            self.wait.wait_for_url_contains("/pim/viewPersonalDetails", timeout=timeout)
            return self.is_visible(self.FIRST_NAME, timeout=timeout)
        except Exception:
            return False

    def get_first_name(self, timeout: int = 10) -> str:
        """Get first name input value once asynchronous hydration completes."""
        self.wait_for_page_readiness()
        try:
            self.wait._get_wait(timeout).until(
                lambda d: (self.get_attribute(self.FIRST_NAME, "value") or "").strip() != ""
            )
        except Exception:
            pass
        return self.get_attribute(self.FIRST_NAME, "value") or ""

    def get_last_name(self) -> str:
        """Get last name input value."""
        return self.get_attribute(self.LAST_NAME, "value") or ""

    def get_nickname(self) -> str:
        """Get nickname input value."""
        return self.get_attribute(self.NICKNAME, "value") or ""

    def update_nickname(self, new_nickname: str) -> None:
        """Modify nickname field and save."""
        logger.info(f"Updating nickname to: '{new_nickname}'")
        self.type_text(self.NICKNAME, new_nickname, clear_first=True)
        self.click_save()

    def update_other_id(self, new_other_id: str) -> None:
        """Modify other ID field and save."""
        logger.info(f"Updating Other ID to: '{new_other_id}'")
        self.type_text(self.OTHER_ID, new_other_id, clear_first=True)
        self.click_save()

    def get_other_id(self) -> str:
        """Get Other ID input value."""
        return self.get_attribute(self.OTHER_ID, "value") or ""

    def click_save(self) -> None:
        """Click the first Save button for Personal Details."""
        logger.info("Saving Personal Details changes.")
        self.click(self.SAVE_BUTTON)
        self.wait_for_page_readiness()
