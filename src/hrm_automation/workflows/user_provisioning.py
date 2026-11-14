"""
User Provisioning Business Workflow Service.
Orchestrates creating system users linked to employees and verifying account visibility.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.data.models.user import SystemUserData
from hrm_automation.pages.admin.add_user_page import AddUserPage
from hrm_automation.pages.admin.user_management_page import UserManagementPage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class UserProvisioningWorkflow:
    """Coordinates Admin user provisioning business journeys."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.list_page = UserManagementPage(driver)
        self.add_page = AddUserPage(driver)

    def provision_user(self, user: SystemUserData) -> None:
        """
        Execute full provisioning flow:
        1. Open Add User view
        2. Enter role, employee linkage, status, username, and password
        3. Submit and verify return to User Management table
        """
        logger.info(f"Executing provision_user workflow for '{user.username}'")
        self.add_page.navigate_to_add_user()
        self.add_page.enter_user_details(user)
        self.add_page.click_save()

        # Wait for redirect back to users table
        self.list_page.wait.wait_for_url_contains("/admin/viewSystemUsers")
        self.list_page.wait_for_page_readiness()

    def provision_and_verify_user(self, user: SystemUserData) -> bool:
        """Provision user and verify presence in system users table."""
        self.provision_user(user)
        self.list_page.search_by_username(user.username)
        return self.list_page.is_user_present_in_table(user.username)
