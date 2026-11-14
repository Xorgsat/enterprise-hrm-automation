"""
Recruitment Business Workflow Service.
Orchestrates candidate creation, candidate pipeline progression, and vacancy linkage.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.data.models.candidate import CandidateData
from hrm_automation.pages.recruitment.add_candidate_page import AddCandidatePage
from hrm_automation.pages.recruitment.candidate_page import CandidatePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class RecruitmentWorkflow:
    """Coordinates Recruitment candidate workflows."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.candidate_page = CandidatePage(driver)
        self.add_page = AddCandidatePage(driver)

    def create_candidate(self, candidate: CandidateData) -> None:
        """Create a candidate and verify redirection."""
        logger.info(f"Creating candidate: {candidate.full_name}")
        self.candidate_page.navigate_to_candidates()
        self.candidate_page.click_add_candidate()
        self.add_page.enter_candidate_details(candidate)
        self.add_page.click_save()

        # Wait for candidate profile or return to candidates list
        self.add_page.wait_for_page_readiness()

    def create_and_verify_candidate(self, candidate: CandidateData) -> bool:
        """Create candidate and verify presence in search table."""
        self.create_candidate(candidate)
        self.candidate_page.navigate_to_candidates()
        self.candidate_page.search_by_name(candidate.first_name)
        return self.candidate_page.is_candidate_present_in_table(candidate.first_name)
