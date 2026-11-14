"""
Leave Management Business Workflow Service.
Orchestrates leave application submission, balance review, and leave status checking.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.pages.leave.apply_leave_page import ApplyLeavePage
from hrm_automation.pages.leave.leave_list_page import LeaveListPage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class LeaveManagementWorkflow:
    """Coordinates Leave domain business workflows."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.list_page = LeaveListPage(driver)
        self.apply_page = ApplyLeavePage(driver)

    def navigate_to_leave_dashboard(self) -> LeaveListPage:
        """Open Leave module and return LeaveListPage."""
        return self.list_page.navigate_to_leave_list()
