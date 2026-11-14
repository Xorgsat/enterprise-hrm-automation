"""
Page Object for OrangeHRM Add Candidate Screen.
Encapsulates /web/index.php/recruitment/addCandidate.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.components.dropdown import DropdownComponent
from hrm_automation.components.toast import ToastComponent
from hrm_automation.core.base_page import BasePage
from hrm_automation.data.models.candidate import CandidateData
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class AddCandidatePage(BasePage):
    """Encapsulates adding a job applicant into the recruitment funnel."""

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")

    EMAIL_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Email']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    CONTACT_NUMBER_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Contact Number']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    KEYWORDS_INPUT = (
        By.XPATH,
        "//label[normalize-space(text())='Keywords']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space(.)='Save' or @type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(.)='Cancel']")
    INPUT_ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-group__message")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.dropdown = DropdownComponent(driver)
        self.toast = ToastComponent(driver)
        self.add_url = f"{settings.base_url}/web/index.php/recruitment/addCandidate"

    def navigate_to_add_candidate(self) -> "AddCandidatePage":
        """Navigate to Add Candidate form."""
        self.open_url(self.add_url)
        self.wait.wait_for_visibility(self.FIRST_NAME_INPUT)
        return self

    def enter_candidate_details(self, candidate: CandidateData) -> "AddCandidatePage":
        """Fill out candidate identity and contact fields."""
        logger.info(f"Populating candidate form for: {candidate.full_name}")
        self.type_text(self.FIRST_NAME_INPUT, candidate.first_name)
        if candidate.middle_name:
            self.type_text(self.MIDDLE_NAME_INPUT, candidate.middle_name)
        self.type_text(self.LAST_NAME_INPUT, candidate.last_name)
        self.type_text(self.EMAIL_INPUT, candidate.email)

        if candidate.contact_number:
            self.type_text(self.CONTACT_NUMBER_INPUT, candidate.contact_number)
        if candidate.keywords:
            self.type_text(self.KEYWORDS_INPUT, candidate.keywords)

        return self

    def click_save(self) -> None:
        """Submit candidate creation form."""
        logger.info("Submitting candidate creation form.")
        self.click(self.SAVE_BUTTON)
        self.wait_for_page_readiness()

    def get_field_errors(self) -> list[str]:
        """Retrieve visible validation error texts."""
        elements = self.find_all(self.INPUT_ERROR_MESSAGES)
        return [e.text.strip() for e in elements if e.text.strip()]
