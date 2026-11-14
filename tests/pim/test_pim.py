"""
Personnel Information Management (PIM) Test Suite.
Validates PIM-001 through PIM-011 covering employee lifecycle, search, modifications, and validations.
"""

import pytest

from hrm_automation.data.factories.employee_factory import EmployeeFactory
from hrm_automation.pages.pim.add_employee_page import AddEmployeePage
from hrm_automation.pages.pim.employee_list_page import EmployeeListPage
from hrm_automation.pages.pim.personal_details_page import PersonalDetailsPage
from hrm_automation.workflows.employee_management import EmployeeManagementWorkflow


@pytest.mark.pim
class TestPIM:
    """Personnel Information Management functional and business validation suite."""

    def test_pim_001_open_employee_list(self, authenticated_driver):
        """PIM-001: Open employee list and verify column headers and table presence."""
        list_page = EmployeeListPage(authenticated_driver)
        list_page.navigate_to_list()

        assert list_page.table.is_table_displayed(), "Employee table was not displayed"
        headers = list_page.table.get_column_headers()
        assert any("Id" in h or "ID" in h for h in headers), f"Expected 'Id' header, got: {headers}"
        assert any("First" in h or "Name" in h for h in headers), (
            f"Expected name header, got: {headers}"
        )

    @pytest.mark.smoke
    def test_pim_002_create_employee_success(self, authenticated_driver, test_namespace):
        """PIM-002: Create employee with unique synthetic data and verify record creation."""
        employee = EmployeeFactory.create(worker_id=test_namespace)
        workflow = EmployeeManagementWorkflow(authenticated_driver)

        assigned_id = workflow.create_employee(employee)
        assert len(assigned_id) > 0, "Expected non-empty employee ID to be assigned"

        details_page = PersonalDetailsPage(authenticated_driver)
        assert details_page.is_loaded(), "Personal Details page did not load after saving employee"
        assert details_page.get_first_name() == employee.first_name

    def test_pim_003_search_employee_by_name(self, authenticated_driver, test_namespace):
        """PIM-003: Search employee list by employee name."""
        employee = EmployeeFactory.create(worker_id=test_namespace)
        workflow = EmployeeManagementWorkflow(authenticated_driver)
        workflow.create_employee(employee)

        list_page = EmployeeListPage(authenticated_driver)
        list_page.navigate_to_list()
        list_page.search_by_name(employee.first_name)

        assert list_page.is_employee_present_in_table(employee.first_name), (
            f"Employee {employee.first_name} was not found in table after search"
        )

    def test_pim_004_search_employee_by_id(self, authenticated_driver, test_namespace):
        """PIM-004: Search employee list by exact Employee ID."""
        employee = EmployeeFactory.create(worker_id=test_namespace)
        workflow = EmployeeManagementWorkflow(authenticated_driver)
        emp_id = workflow.create_employee(employee)

        list_page = EmployeeListPage(authenticated_driver)
        list_page.navigate_to_list()
        list_page.search_by_id(emp_id)

        assert list_page.is_employee_present_in_table(emp_id), (
            f"Employee ID {emp_id} was not found in table after search"
        )

    def test_pim_005_modify_employee_details(self, authenticated_driver, test_namespace):
        """PIM-005 & PIM-006: Modify employee nickname and verify persistence."""
        employee = EmployeeFactory.create(worker_id=test_namespace)
        workflow = EmployeeManagementWorkflow(authenticated_driver)
        workflow.create_employee(employee)

        details_page = PersonalDetailsPage(authenticated_driver)
        updated_nickname = f"Upd_{employee.nickname}"
        details_page.update_nickname(updated_nickname)

        # Refresh page to verify database persistence
        authenticated_driver.refresh()
        details_page.wait_for_page_readiness()

        assert details_page.get_nickname() == updated_nickname, (
            f"Expected updated nickname '{updated_nickname}', found '{details_page.get_nickname()}'"
        )

    @pytest.mark.negative
    def test_pim_007_missing_first_name(self, authenticated_driver, test_namespace):
        """PIM-007: Omitting first name displays inline 'Required' validation error."""
        add_page = AddEmployeePage(authenticated_driver)
        add_page.navigate_to_add_employee()

        # Enter only last name
        add_page.type_text(add_page.LAST_NAME_INPUT, f"Test_{test_namespace}")
        add_page.click_save()

        errors = add_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"

    @pytest.mark.negative
    def test_pim_008_missing_last_name(self, authenticated_driver, test_namespace):
        """PIM-008: Omitting last name displays inline 'Required' validation error."""
        add_page = AddEmployeePage(authenticated_driver)
        add_page.navigate_to_add_employee()

        # Enter only first name
        add_page.type_text(add_page.FIRST_NAME_INPUT, f"Aut_{test_namespace}")
        add_page.click_save()

        errors = add_page.get_field_errors()
        assert "Required" in errors, f"Expected 'Required' validation error, got: {errors}"

    @pytest.mark.negative
    def test_pim_010_search_nonexistent_employee(self, authenticated_driver):
        """PIM-010: Searching for non-existent employee displays 'No Records Found'."""
        list_page = EmployeeListPage(authenticated_driver)
        list_page.navigate_to_list()
        list_page.search_by_id("999999999_NON_EXISTENT")

        records_text = list_page.get_records_count_text()
        assert "No Records Found" in records_text or list_page.table.get_row_count() == 0, (
            f"Expected zero records, found: {records_text}"
        )

    def test_pim_011_cancel_employee_creation(self, authenticated_driver):
        """PIM-011: Clicking cancel aborts employee creation and returns to employee list."""
        add_page = AddEmployeePage(authenticated_driver)
        add_page.navigate_to_add_employee()
        add_page.click_cancel()

        assert "/pim/viewEmployeeList" in authenticated_driver.current_url
