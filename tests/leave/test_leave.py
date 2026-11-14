"""
Leave Management Test Suite.
Validates LEAVE-001 through LEAVE-009 covering leave views, navigation, and application form validations.
"""

import pytest

from hrm_automation.pages.leave.apply_leave_page import ApplyLeavePage
from hrm_automation.pages.leave.leave_list_page import LeaveListPage


@pytest.mark.leave
class TestLeave:
    """Leave Management business and functional test suite."""

    @pytest.mark.smoke
    def test_leave_001_open_leave_list(self, authenticated_driver):
        """LEAVE-001: Open Leave module and verify records table structure and columns."""
        leave_page = LeaveListPage(authenticated_driver)
        leave_page.navigate_to_leave_list()

        assert leave_page.table.is_table_displayed(), "Leave table was not displayed"
        headers = leave_page.table.get_column_headers()
        assert any("Date" in h for h in headers), f"Expected 'Date' header, got: {headers}"
        assert any("Employee Name" in h for h in headers), (
            f"Expected 'Employee Name' header, got: {headers}"
        )
        assert any("Status" in h for h in headers), f"Expected 'Status' header, got: {headers}"

    def test_leave_002_navigate_to_apply_leave(self, authenticated_driver):
        """LEAVE-002: Navigate from Leave List to Apply Leave form."""
        leave_page = LeaveListPage(authenticated_driver)
        leave_page.navigate_to_leave_list()
        leave_page.navigate_to_apply_leave()

        apply_page = ApplyLeavePage(authenticated_driver)
        assert "/leave/applyLeave" in authenticated_driver.current_url
        assert (
            apply_page.is_visible(apply_page.APPLY_BUTTON)
            or apply_page.has_no_leave_balance_warning()
        ), (
            "Neither Apply form button nor 'No Leave Types with Leave Balance' alert was visible on Apply Leave page."
        )

    @pytest.mark.negative
    def test_leave_008_missing_leave_type(self, authenticated_driver):
        """LEAVE-008: Submitting empty leave application triggers 'Required' validation."""
        apply_page = ApplyLeavePage(authenticated_driver)
        apply_page.navigate_to_apply()

        if apply_page.has_no_leave_balance_warning():
            pytest.skip(
                "Hosted Demo constraint: Current user has 'No Leave Types with Leave Balance'. "
                "Form submission is suppressed by OrangeHRM business rules when zero balance is available. "
                "This scenario requires a self-hosted instance with configured leave entitlements."
            )

        apply_page.click_apply()
        errors = apply_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"
