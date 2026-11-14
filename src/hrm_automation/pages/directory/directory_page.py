"""
Page Object for OrangeHRM Employee Directory Screen.
Encapsulates /web/index.php/directory/viewDirectory.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.components.dropdown import DropdownComponent
from hrm_automation.components.sidebar import SidebarComponent
from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class DirectoryPage(BasePage):
    """Encapsulates the company-wide employee directory."""

    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space(.)='Reset']")
    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Employee Name']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    DIRECTORY_CARDS = (By.CSS_SELECTOR, ".oxd-grid-item .orangehrm-directory-card")
    CARD_HEADER = (By.CSS_SELECTOR, ".orangehrm-directory-card-header")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.sidebar = SidebarComponent(driver)
        self.dropdown = DropdownComponent(driver)
        self.url = f"{settings.base_url}/web/index.php/directory/viewDirectory"

    def navigate_to_directory(self) -> "DirectoryPage":
        """Navigate to Directory view."""
        logger.info(f"Navigating to Directory: {self.url}")
        self.open_url(self.url)
        self.wait.wait_for_visibility(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()
        return self

    def is_directory_displayed(self) -> bool:
        """Check if directory search controls are visible."""
        return "/directory/viewDirectory" in self.current_url and self.is_visible(
            self.SEARCH_BUTTON
        )

    def get_directory_card_count(self) -> int:
        """Return number of rendered employee directory cards."""
        return len(self.find_all(self.DIRECTORY_CARDS, timeout=5))
