"""
Modal Dialog Component.
Encapsulates OrangeHRM confirmation sheets (.oxd-dialog-sheet).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.core.base_page import BasePage


class ModalComponent(BasePage):
    """Encapsulates interaction with popup modal dialogs."""

    DIALOG_SHEET = (By.CSS_SELECTOR, ".oxd-dialog-sheet")
    TITLE = (By.CSS_SELECTOR, ".oxd-dialog-sheet .oxd-text--card-title")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, ".oxd-dialog-sheet button.oxd-button--label-danger")
    CANCEL_BUTTON = (By.CSS_SELECTOR, ".oxd-dialog-sheet button.oxd-button--text")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_modal_displayed(self, timeout: int = 5) -> bool:
        """Check if modal dialog is open."""
        return self.is_visible(self.DIALOG_SHEET, timeout=timeout)

    def confirm(self) -> None:
        """Click confirmation action button (e.g., 'Yes, Delete')."""
        self.click(self.CONFIRM_BUTTON)
        self.wait.wait_for_invisibility(self.DIALOG_SHEET)

    def cancel(self) -> None:
        """Dismiss modal without executing action."""
        self.click(self.CANCEL_BUTTON)
        self.wait.wait_for_invisibility(self.DIALOG_SHEET)
