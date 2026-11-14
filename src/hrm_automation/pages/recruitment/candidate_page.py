"""
Page Object for OrangeHRM Recruitment Candidates Screen.
Encapsulates /web/index.php/recruitment/viewCandidates.
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


class CandidatePage(BasePage):
    """Encapsulates the /web/index.php/recruitment/viewCandidates interface."""

    ADD_BUTTON = (By.XPATH, "//button[normalize-space(.)='Add' or contains(.,'Add')]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space(.)='Reset']")
    CANDIDATE_NAME_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Candidate Name']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.sidebar = SidebarComponent(driver)
        self.table = DataTableComponent(driver)
        self.dropdown = DropdownComponent(driver)
        self.url = f"{settings.base_url}/web/index.php/recruitment/viewCandidates"

    def navigate_to_candidates(self) -> "CandidatePage":
        """Navigate to Candidates view."""
        logger.info(f"Navigating to Candidates: {self.url}")
        self.open_url(self.url)
        self.wait.wait_for_visibility(self.ADD_BUTTON)
        self.wait_for_page_readiness()
        return self

    def click_add_candidate(self) -> None:
        """Click Add button to open candidate creation form."""
        logger.info("Opening Add Candidate form.")
        self.click(self.ADD_BUTTON)
        self.wait.wait_for_url_contains("/recruitment/addCandidate")

    def search_by_name(self, name: str) -> None:
        """Filter candidates by name."""
        logger.info(f"Searching candidates by name: '{name}'")
        self.type_text(self.CANDIDATE_NAME_INPUT, name, clear_first=True)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_page_readiness()

    def is_candidate_present_in_table(self, candidate_name: str) -> bool:
        """Check if candidate row is present in the table."""
        return self.table.find_row_index_by_text(candidate_name) is not None
