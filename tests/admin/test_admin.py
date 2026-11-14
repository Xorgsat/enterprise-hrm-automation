"""
Admin and User Management Test Suite.
Validates ADM-001 through ADM-010 covering user search, role/status filtering, and form validations.
"""

import pytest

from hrm_automation.pages.admin.add_user_page import AddUserPage
from hrm_automation.pages.admin.user_management_page import UserManagementPage


@pytest.mark.admin
class TestAdminUserManagement:
    """System User Administration functional test suite."""

    @pytest.mark.smoke
    def test_adm_001_open_user_management(self, authenticated_driver):
        """ADM-001: Open user management and verify table structure and action controls."""
        admin_page = UserManagementPage(authenticated_driver)
        admin_page.navigate_to_user_management()

        assert admin_page.table.is_table_displayed(), "System users table was not displayed"
        headers = admin_page.table.get_column_headers()
        assert "Username" in headers, f"Expected 'Username' in headers, got: {headers}"
        assert "User Role" in headers, f"Expected 'User Role' in headers, got: {headers}"
        assert "Status" in headers, f"Expected 'Status' in headers, got: {headers}"

    def test_adm_002_search_existing_admin_user(self, authenticated_driver):
        """ADM-002: Search users table by standard 'Admin' username."""
        admin_page = UserManagementPage(authenticated_driver)
        admin_page.navigate_to_user_management()
        admin_page.search_by_username("Admin")

        assert admin_page.is_user_present_in_table("Admin"), (
            "User 'Admin' not found in filtered table"
        )

    def test_adm_003_filter_users_by_role(self, authenticated_driver):
        """ADM-003: Filter users table by User Role 'Admin'."""
        admin_page = UserManagementPage(authenticated_driver)
        admin_page.navigate_to_user_management()
        admin_page.filter_by_role("Admin")

        assert admin_page.table.get_row_count() > 0, "No records returned for Admin role filter"

    def test_adm_004_filter_users_by_status(self, authenticated_driver):
        """ADM-004: Filter users table by Status 'Enabled'."""
        admin_page = UserManagementPage(authenticated_driver)
        admin_page.navigate_to_user_management()
        admin_page.filter_by_status("Enabled")

        assert admin_page.table.get_row_count() > 0, "No records returned for Enabled status filter"

    @pytest.mark.negative
    def test_adm_007_missing_required_username(self, authenticated_driver):
        """ADM-007: Submitting add user form without username triggers 'Required' validation."""
        add_user_page = AddUserPage(authenticated_driver)
        add_user_page.navigate_to_add_user()
        add_user_page.click_save()

        errors = add_user_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"

    @pytest.mark.negative
    def test_adm_009_missing_employee_association(self, authenticated_driver):
        """ADM-009: Submitting add user form without employee linkage triggers 'Required'."""
        add_user_page = AddUserPage(authenticated_driver)
        add_user_page.navigate_to_add_user()
        add_user_page.click_save()

        errors = add_user_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"
