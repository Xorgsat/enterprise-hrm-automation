"""
Recruitment and Candidate Management Test Suite.
Validates REC-001 through REC-009 covering candidate creation, search, and form validations.
"""

import pytest

from hrm_automation.data.factories.candidate_factory import CandidateFactory
from hrm_automation.pages.recruitment.add_candidate_page import AddCandidatePage
from hrm_automation.pages.recruitment.candidate_page import CandidatePage
from hrm_automation.workflows.recruitment import RecruitmentWorkflow


@pytest.mark.recruitment
class TestRecruitment:
    """Recruitment candidate pipeline functional test suite."""

    @pytest.mark.smoke
    def test_rec_001_open_candidates_list(self, authenticated_driver):
        """REC-001: Open Recruitment module and verify candidates table structure."""
        candidate_page = CandidatePage(authenticated_driver)
        candidate_page.navigate_to_candidates()

        assert candidate_page.table.is_table_displayed(), "Candidates table was not displayed"
        headers = candidate_page.table.get_column_headers()
        assert any("Candidate" in h for h in headers), (
            f"Expected 'Candidate' in headers, got: {headers}"
        )
        assert any("Status" in h for h in headers), f"Expected 'Status' in headers, got: {headers}"

    @pytest.mark.smoke
    def test_rec_003_create_candidate_success(self, authenticated_driver, test_namespace):
        """REC-003: Create candidate with unique details and verify successful save."""
        candidate = CandidateFactory.create(worker_id=test_namespace)
        workflow = RecruitmentWorkflow(authenticated_driver)
        workflow.create_candidate(candidate)

        # Verify page transition away from new blank add form into candidate record
        assert (
            "/recruitment/addCandidate/" in authenticated_driver.current_url
            or "/viewCandidates" in authenticated_driver.current_url
        )

    def test_rec_004_search_candidate_by_name(self, authenticated_driver, test_namespace):
        """REC-004: Search candidates table by candidate name."""
        candidate = CandidateFactory.create(worker_id=test_namespace)
        workflow = RecruitmentWorkflow(authenticated_driver)
        workflow.create_candidate(candidate)

        candidate_page = CandidatePage(authenticated_driver)
        candidate_page.navigate_to_candidates()
        candidate_page.search_by_name(candidate.first_name)

        assert candidate_page.is_candidate_present_in_table(candidate.first_name)

    @pytest.mark.negative
    def test_rec_008_missing_candidate_name(self, authenticated_driver):
        """REC-008: Submitting empty candidate form triggers 'Required' validation."""
        add_page = AddCandidatePage(authenticated_driver)
        add_page.navigate_to_add_candidate()
        add_page.click_save()

        errors = add_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"

    @pytest.mark.negative
    def test_rec_009_invalid_email_format(self, authenticated_driver):
        """REC-009: Submitting invalid email triggers email format validation."""
        add_page = AddCandidatePage(authenticated_driver)
        add_page.navigate_to_add_candidate()
        add_page.type_text(add_page.FIRST_NAME_INPUT, "John")
        add_page.type_text(add_page.LAST_NAME_INPUT, "Doe")
        add_page.type_text(add_page.EMAIL_INPUT, "not-an-email-address")
        add_page.click_save()

        errors = add_page.get_field_errors()
        assert any("Expected format" in err or "format" in err.lower() for err in errors), (
            f"Expected email format validation error, got: {errors}"
        )
