"""
Sidebar Navigation Component.
Encapsulates OrangeHRM responsive sidebar menu (.oxd-sidepanel).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class SidebarComponent(BasePage):
    """Encapsulates interaction with the global sidebar navigation menu."""

    SIDEBAR_CONTAINER = (By.CSS_SELECTOR, ".oxd-sidepanel")
    MENU_ITEMS = (By.CSS_SELECTOR, ".oxd-main-menu-item")
    TOGGLE_BUTTON = (By.CSS_SELECTOR, "button.oxd-main-menu-button")
    SEARCH_INPUT = (By.CSS_SELECTOR, ".oxd-main-menu-search input")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def navigate_to_module(self, module_name: str) -> None:
        """Click on the sidebar menu link matching the module name."""
        logger.info(f"Navigating via sidebar to module: '{module_name}'")
        # Ensure sidebar is present
        self.wait.wait_for_visibility(self.SIDEBAR_CONTAINER)

        # Scoped locator: find anchor item containing span with exact module name
        module_locator = (
            By.XPATH,
            f"//aside[contains(@class,'oxd-sidepanel')]//a[contains(@class,'oxd-main-menu-item')][.//span[normalize-space(text())='{module_name}'] or normalize-space(.)='{module_name}']",
        )
        self.click(module_locator)
        self.wait_for_page_readiness()

    def get_available_modules(self) -> list[str]:
        """Return list of all visible module names in the sidebar."""
        elements = self.find_all(self.MENU_ITEMS)
        names = []
        for elem in elements:
            text = elem.text.strip()
            if text:
                names.append(text)
        return names
