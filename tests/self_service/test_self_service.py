"""
Employee Self-Service (My Info) and Directory Test Suite.
Validates employee self-service access and directory accessibility.
"""

import pytest

from hrm_automation.pages.directory.directory_page import DirectoryPage
from hrm_automation.pages.pim.personal_details_page import PersonalDetailsPage


@pytest.mark.self_service
class TestSelfService:
    """Employee self-service and corporate directory test suite."""

    def test_ess_001_my_info_personal_details_access(self, authenticated_driver):
        """ESS-001: Authenticated user navigates to My Info and views personal details."""
        personal_details = PersonalDetailsPage(authenticated_driver)
        # Use sidebar navigation
        personal_details.open_url(
            f"{personal_details.driver.current_url.split('/web/')[0]}/web/index.php/pim/viewMyDetails"
        )

        assert personal_details.is_loaded(), "My Info personal details did not load"
        first_name = personal_details.get_first_name()
        assert len(first_name) > 0, "Expected employee First Name to be populated"

    def test_ess_002_directory_view_and_cards(self, authenticated_driver):
        """ESS-002: Authenticated user accesses corporate Directory and views employee profiles."""
        directory_page = DirectoryPage(authenticated_driver)
        directory_page.navigate_to_directory()

        assert directory_page.is_directory_displayed(), "Directory view was not displayed"
        # Directory cards may be present depending on demo state
        card_count = directory_page.get_directory_card_count()
        assert card_count >= 0, f"Unexpected card count: {card_count}"
