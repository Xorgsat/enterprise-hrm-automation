"""
Employee Management Business Workflow Service.
Orchestrates employee creation, verification, modification, and search business journeys.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.core.exceptions import WorkflowExecutionException
from hrm_automation.data.models.employee import EmployeeData
from hrm_automation.pages.pim.add_employee_page import AddEmployeePage
from hrm_automation.pages.pim.employee_list_page import EmployeeListPage
from hrm_automation.pages.pim.personal_details_page import PersonalDetailsPage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class EmployeeManagementWorkflow:
    """Coordinates PIM employee lifecycle journeys."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.list_page = EmployeeListPage(driver)
        self.add_page = AddEmployeePage(driver)
        self.details_page = PersonalDetailsPage(driver)

    def create_employee(self, employee: EmployeeData) -> str:
        """
        Execute end-to-end employee creation:
        1. Open Add Employee form
        2. Populate details
        3. Submit and wait for redirect to Personal Details
        4. Return the assigned employee ID
        """
        logger.info(f"Executing create_employee workflow for: {employee.full_name}")
        self.add_page.navigate_to_add_employee()
        self.add_page.enter_employee_details(employee)
        assigned_id = self.add_page.get_assigned_employee_id()
        self.add_page.click_save()

        # Wait for redirect to personal details view
        if not self.details_page.is_loaded():
            raise WorkflowExecutionException(
                f"Employee creation failed to transition to personal details view. Current URL: {self.driver.current_url}"
            )

        final_id = employee.employee_id or assigned_id
        logger.info(f"Employee {employee.full_name} created successfully with ID: {final_id}")
        return final_id

    def create_employee_and_verify(self, employee: EmployeeData) -> bool:
        """Create employee and verify presence in the PIM employee list."""
        emp_id = self.create_employee(employee)
        self.list_page.navigate_to_list()
        self.list_page.search_by_id(emp_id)
        is_present = self.list_page.is_employee_present_in_table(emp_id)
        if not is_present:
            # Fallback search by first name in case ID formatting differs
            self.list_page.reset_search()
            self.list_page.search_by_name(employee.first_name)
            is_present = self.list_page.is_employee_present_in_table(employee.first_name)

        return is_present
