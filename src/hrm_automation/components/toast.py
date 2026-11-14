"""
Toast Notification Component.
Encapsulates OrangeHRM floating feedback messages (.oxd-toast).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class ToastComponent(BasePage):
    """Encapsulates OrangeHRM toast notifications."""

    TOAST_CONTAINER = (By.CSS_SELECTOR, ".oxd-toast")
    TOAST_TITLE = (By.CSS_SELECTOR, ".oxd-toast-content-title")
    TOAST_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")
    TOAST_CLOSE_BTN = (By.CSS_SELECTOR, ".oxd-toast-close")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_toast_displayed(self, timeout: int = 5) -> bool:
        """Check if any toast is currently visible."""
        return self.is_visible(self.TOAST_CONTAINER, timeout=timeout)

    def get_toast_message(self, timeout: int = 5) -> str:
        """Retrieve the primary body text of the visible toast."""
        return self.get_text(self.TOAST_MESSAGE, timeout=timeout)

    def get_toast_title(self, timeout: int = 5) -> str:
        """Retrieve the title text (e.g. 'Success', 'Info', 'Error') of the visible toast."""
        return self.get_text(self.TOAST_TITLE, timeout=timeout)

    def wait_for_toast_dismissal(self, timeout: int = 6) -> bool:
        """Wait until the toast animation fades and unmounts."""
        return self.wait.wait_for_invisibility(self.TOAST_CONTAINER, timeout=timeout)
