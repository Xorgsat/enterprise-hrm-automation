"""
Custom Dropdown Component.
Encapsulates OrangeHRM non-native dropdown controls (.oxd-select-wrapper).
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class DropdownComponent(BasePage):
    """Handles interaction with custom Vue-based .oxd-select components."""

    DROPDOWN_TEXT = (By.CSS_SELECTOR, ".oxd-select-text-input")
    DROPDOWN_MENU = (By.CSS_SELECTOR, ".oxd-select-dropdown")
    DROPDOWN_OPTIONS = (By.CSS_SELECTOR, ".oxd-select-option")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def select_by_label_and_text(self, form_label: str, option_text: str) -> None:
        """
        Locate a dropdown by its preceding form label (e.g. 'User Role', 'Status', 'Job Title')
        and select the option matching option_text.
        """
        logger.info(f"Selecting '{option_text}' from dropdown labeled '{form_label}'")

        # Scoped locator: find label, traverse to sibling div containing .oxd-select-text
        dropdown_wrapper = (
            By.XPATH,
            f"//label[normalize-space(text())='{form_label}']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text')]",
        )
        self.click(dropdown_wrapper)

        # Wait for options dropdown to appear
        self.wait.wait_for_visibility(self.DROPDOWN_MENU, timeout=5)
        time.sleep(0.2)  # Allow animation to settle

        # Click the option matching option_text
        option_locator = (
            By.XPATH,
            f"//div[contains(@class,'oxd-select-dropdown')]//div[contains(@class,'oxd-select-option')][span[normalize-space(text())='{option_text}'] or normalize-space(text())='{option_text}']",
        )
        self.click(option_locator)
        self.wait.wait_for_invisibility(self.DROPDOWN_MENU, timeout=5)

    def select_by_container(self, container_locator: tuple[By, str], option_text: str) -> None:
        """Select an option from a specific dropdown container locator."""
        self.click(container_locator)
        self.wait.wait_for_visibility(self.DROPDOWN_MENU, timeout=5)
        time.sleep(0.2)

        option_locator = (
            By.XPATH,
            f"//div[contains(@class,'oxd-select-dropdown')]//div[contains(@class,'oxd-select-option')][span[normalize-space(text())='{option_text}'] or normalize-space(text())='{option_text}']",
        )
        self.click(option_locator)
        self.wait.wait_for_invisibility(self.DROPDOWN_MENU, timeout=5)

    def get_selected_text_for_label(self, form_label: str) -> str:
        """Retrieve the currently selected value in a dropdown associated with a label."""
        dropdown_text_locator = (
            By.XPATH,
            f"//label[normalize-space(text())='{form_label}']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text-input')]",
        )
        return self.get_text(dropdown_text_locator)
