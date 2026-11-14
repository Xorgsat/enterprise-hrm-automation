"""
Authentication and Session Lifecycle Test Suite.
Validates AUTH-001 through AUTH-010 covering positive, negative, and session-boundary scenarios.
"""

import pytest

from config.settings import settings
from hrm_automation.pages.auth.login_page import LoginPage
from hrm_automation.workflows.authentication import AuthenticationWorkflow


@pytest.mark.authentication
class TestAuthentication:
    """Test suite for authentication, authorization boundary, and session lifecycle."""

    @pytest.mark.smoke
    def test_auth_001_valid_admin_login(self, driver):
        """AUTH-001: Valid administrator login redirects to Dashboard with active session."""
        auth_workflow = AuthenticationWorkflow(driver)
        dashboard_page = auth_workflow.login_as_admin()

        assert dashboard_page.is_dashboard_displayed(), (
            "Dashboard was not displayed after valid login"
        )
        assert len(dashboard_page.get_logged_in_user_name()) > 0, (
            "Logged-in user avatar name was empty"
        )

    @pytest.mark.negative
    def test_auth_002_invalid_username(self, driver):
        """AUTH-002: Login with non-existent username displays 'Invalid credentials' alert."""
        auth_workflow = AuthenticationWorkflow(driver)
        login_page = auth_workflow.login_expecting_failure(
            username="NonExistentUser_9999", password=settings.admin_password
        )

        alert_text = login_page.get_alert_error()
        assert "Invalid credentials" in alert_text, f"Unexpected alert text: '{alert_text}'"
        assert login_page.is_on_login_page(), "Browser navigated away from login page unexpectedly"

    @pytest.mark.negative
    def test_auth_003_invalid_password(self, driver):
        """AUTH-003: Login with incorrect password displays 'Invalid credentials' alert."""
        auth_workflow = AuthenticationWorkflow(driver)
        login_page = auth_workflow.login_expecting_failure(
            username=settings.admin_username, password="WrongPassword_12345!"
        )

        alert_text = login_page.get_alert_error()
        assert "Invalid credentials" in alert_text, f"Unexpected alert text: '{alert_text}'"
        assert login_page.is_on_login_page()

    @pytest.mark.negative
    def test_auth_004_empty_username(self, driver):
        """AUTH-004: Missing username displays inline 'Required' validation error."""
        auth_workflow = AuthenticationWorkflow(driver)
        login_page = auth_workflow.login_expecting_failure(
            username=None, password=settings.admin_password
        )

        errors = login_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"
        assert login_page.is_on_login_page()

    @pytest.mark.negative
    def test_auth_005_empty_password(self, driver):
        """AUTH-005: Missing password displays inline 'Required' validation error."""
        auth_workflow = AuthenticationWorkflow(driver)
        login_page = auth_workflow.login_expecting_failure(
            username=settings.admin_username, password=None
        )

        errors = login_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"
        assert login_page.is_on_login_page()

    @pytest.mark.negative
    def test_auth_006_both_credentials_empty(self, driver):
        """AUTH-006: Submitting empty form displays dual 'Required' validation errors."""
        auth_workflow = AuthenticationWorkflow(driver)
        login_page = auth_workflow.login_expecting_failure(username=None, password=None)

        errors = login_page.get_field_errors()
        assert len(errors) >= 2, f"Expected at least two 'Required' errors, got: {errors}"
        assert all(err == "Required" for err in errors[:2])
        assert login_page.is_on_login_page()

    @pytest.mark.smoke
    def test_auth_007_logout_workflow(self, driver):
        """AUTH-007: Safe logout terminates session and redirects to login."""
        auth_workflow = AuthenticationWorkflow(driver)
        auth_workflow.login_as_admin()
        login_page = auth_workflow.logout_and_verify()

        assert login_page.is_on_login_page(), "User was not returned to login page upon logout"

    @pytest.mark.negative
    @pytest.mark.authorization
    def test_auth_008_protected_page_without_auth(self, driver):
        """AUTH-008: Accessing protected page directly without auth redirects to login."""
        protected_url = f"{settings.base_url}/web/index.php/admin/viewSystemUsers"
        driver.get(protected_url)

        login_page = LoginPage(driver)
        # Should be redirected to login
        login_page.wait.wait_for_url_contains("/auth/login")
        assert login_page.is_on_login_page(), (
            f"Protected route did not redirect to login. URL: {driver.current_url}"
        )

    @pytest.mark.authorization
    def test_auth_009_browser_back_after_logout(self, driver):
        """AUTH-009: Back button navigation after logout does not restore authenticated session."""
        auth_workflow = AuthenticationWorkflow(driver)
        auth_workflow.login_as_admin()
        login_page = auth_workflow.logout_and_verify()

        # Attempt browser back
        driver.back()

        # Verify server enforces session revocation upon request
        driver.refresh()
        login_page.wait.wait_for_url_contains("/auth/login")
        assert login_page.is_on_login_page(), (
            f"Backward navigation breached session boundary! Current URL: {driver.current_url}"
        )

    @pytest.mark.smoke
    def test_auth_010_authenticated_navigation(self, driver):
        """AUTH-010: Session persistence across module navigation."""
        auth_workflow = AuthenticationWorkflow(driver)
        dashboard_page = auth_workflow.login_as_admin()

        # Navigate to PIM via sidebar and verify session persists
        dashboard_page.sidebar.navigate_to_module("PIM")
        assert "/pim/viewEmployeeList" in driver.current_url

        # Navigate back to Dashboard via sidebar
        dashboard_page.sidebar.navigate_to_module("Dashboard")
        assert "/dashboard/index" in driver.current_url
