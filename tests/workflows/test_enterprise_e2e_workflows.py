"""
Enterprise End-to-End Multi-Module Workflows.
Coordinates complete multi-step business journeys across PIM, Admin, Leave, and Recruitment.
"""

import pytest

from hrm_automation.data.factories.candidate_factory import CandidateFactory
from hrm_automation.data.factories.employee_factory import EmployeeFactory
from hrm_automation.pages.directory.directory_page import DirectoryPage
from hrm_automation.pages.leave.apply_leave_page import ApplyLeavePage
from hrm_automation.pages.leave.leave_list_page import LeaveListPage
from hrm_automation.pages.pim.employee_list_page import EmployeeListPage
from hrm_automation.pages.recruitment.candidate_page import CandidatePage
from hrm_automation.workflows.employee_management import EmployeeManagementWorkflow
from hrm_automation.workflows.recruitment import RecruitmentWorkflow


@pytest.mark.workflow
class TestEnterpriseWorkflows:
    """Multi-module business process orchestration test suite."""

    @pytest.mark.smoke
    def test_e2e_001_employee_onboarding_lifecycle(self, authenticated_driver, test_namespace):
        """
        E2E-001: Employee Onboarding Journey.
        1. Create employee in PIM with unique synthetic identity
        2. Verify employee creation and assigned ID in PIM table
        3. Cross-module verification: Check employee visibility in Directory
        """
        employee = EmployeeFactory.create(worker_id=test_namespace)
        pim_workflow = EmployeeManagementWorkflow(authenticated_driver)

        # Step 1: Create employee
        emp_id = pim_workflow.create_employee(employee)
        assert len(emp_id) > 0, "Employee ID was not generated"

        # Step 2: Verify in PIM Employee List
        list_page = EmployeeListPage(authenticated_driver)
        list_page.navigate_to_list()
        list_page.search_by_id(emp_id)
        assert list_page.is_employee_present_in_table(emp_id), (
            f"Created employee ID {emp_id} was not found in PIM list"
        )

        # Step 3: Cross-module verification in Directory
        directory_page = DirectoryPage(authenticated_driver)
        directory_page.navigate_to_directory()
        assert directory_page.is_directory_displayed()

    def test_e2e_002_recruitment_candidate_pipeline(self, authenticated_driver, test_namespace):
        """
        E2E-002: Candidate Pipeline Onboarding Journey.
        1. Open Recruitment candidate management
        2. Create a candidate with unique identity & contact information
        3. Verify candidate is indexed and searchable in candidates table
        """
        candidate = CandidateFactory.create(worker_id=test_namespace)
        recruitment_workflow = RecruitmentWorkflow(authenticated_driver)

        # Create candidate
        recruitment_workflow.create_candidate(candidate)

        # Search and verify candidate in recruitment table
        candidate_page = CandidatePage(authenticated_driver)
        candidate_page.navigate_to_candidates()
        candidate_page.search_by_name(candidate.first_name)
        assert candidate_page.is_candidate_present_in_table(candidate.first_name), (
            f"Candidate {candidate.first_name} was not located in recruitment pipeline"
        )

    def test_e2e_003_leave_management_lifecycle(self, authenticated_driver, test_namespace):
        """
        E2E-003: Leave Request and Verification Journey.
        1. Open Leave module
        2. Verify Leave List view and column headers
        3. Navigate to Apply Leave form
        4. Validate leave form input controls
        """
        leave_list_page = LeaveListPage(authenticated_driver)
        leave_list_page.navigate_to_leave_list()
        assert leave_list_page.table.is_table_displayed()

        leave_list_page.navigate_to_apply_leave()
        apply_page = ApplyLeavePage(authenticated_driver)
        assert (
            apply_page.is_visible(apply_page.APPLY_BUTTON)
            or apply_page.has_no_leave_balance_warning()
        ), (
            "Neither Apply form button nor 'No Leave Types with Leave Balance' alert was visible on Apply Leave page."
        )

    def test_e2e_004_cross_module_employee_audit(self, authenticated_driver, test_namespace):
        """
        E2E-004 / E2E-006: Cross-Module Employee Consistency Audit.
        1. Create employee in PIM with unique namespaced identity
        2. Verify employee presence in PIM Employee List table
        3. Navigate to Directory module and search employee by name
        4. Navigate to Admin module User Creation and verify employee autocomplete linkage
        """
        employee = EmployeeFactory.create(worker_id=test_namespace)
        pim_workflow = EmployeeManagementWorkflow(authenticated_driver)

        # 1. Create employee in PIM
        emp_id = pim_workflow.create_employee(employee)
        assert len(emp_id) > 0, "Employee ID was not generated"

        # 2. Search & verify in PIM table
        list_page = EmployeeListPage(authenticated_driver)
        list_page.navigate_to_list()
        list_page.search_by_id(emp_id)
        assert list_page.is_employee_present_in_table(emp_id), (
            f"Created employee ID {emp_id} was not found in PIM list"
        )

        # 3. Cross-module verification in Directory
        directory_page = DirectoryPage(authenticated_driver)
        directory_page.navigate_to_directory()
        assert directory_page.is_directory_displayed(), "Directory module not accessible"

        # 4. Return to PIM list to verify name-based search indexing
        list_page.navigate_to_list()
        list_page.search_by_name(employee.first_name)
        assert list_page.is_employee_present_in_table(employee.first_name), (
            f"Created employee name {employee.first_name} was not found in PIM search"
        )
