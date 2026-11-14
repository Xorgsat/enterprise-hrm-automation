# Automation Platform Architecture & Engineering Design

## 1. Architectural Philosophy & Charter
The Enterprise Human Resource Management (HRM) Quality Engineering Platform is engineered as a decoupled, resilient, observable test automation platform. Rather than writing fragile browser scripts, the architecture provides a maintainable test harness designed to support continuous integration and cross-functional quality gates.

```mermaid
flowchart TD
    subgraph Test_Layer [1. Test Scenarios Layer]
        T_Auth[Authentication Tests]
        T_PIM[PIM Employee Tests]
        T_Admin[User Admin Tests]
        T_Leave[Leave Management Tests]
        T_Rec[Recruitment Tests]
        T_E2E[End-to-End Workflows]
    end

    subgraph Workflow_Layer [2. Business Workflow Services]
        W_Auth[AuthenticationWorkflow]
        W_Emp[EmployeeManagementWorkflow]
        W_User[UserProvisioningWorkflow]
        W_Leave[LeaveManagementWorkflow]
        W_Rec[RecruitmentWorkflow]
    end

    subgraph Page_Layer [3. Page Objects & UI Components]
        P_Login[LoginPage]
        P_Dash[DashboardPage]
        P_PIM[EmployeeListPage & AddEmployeePage]
        P_Admin[UserManagementPage & AddUserPage]
        P_Leave[LeaveListPage & ApplyLeavePage]
        P_Rec[CandidatePage & AddCandidatePage]
        C_Table[DataTableComponent]
        C_Drop[DropdownComponent]
        C_Toast[ToastComponent]
        C_Side[SidebarComponent]
    end

    subgraph Core_Layer [4. Core Synchronization & Engine]
        BP[BasePage Primitive Engine]
        WM[WaitManager Explicit Waits]
        EX[Custom HRM Exceptions]
    end

    subgraph Infra_Layer [5. Infrastructure & Data Factory]
        DF[DriverFactory - Selenium Manager]
        CFG[FrameworkSettings - Pydantic]
        DFact[EmployeeFactory / UserFactory]
        SH[Diagnostic Screenshot & Allure Hooks]
    end

    Test_Layer --> Workflow_Layer
    Test_Layer --> Page_Layer
    Workflow_Layer --> Page_Layer
    Page_Layer --> Core_Layer
    Page_Layer --> C_Table
    Page_Layer --> C_Drop
    Page_Layer --> C_Toast
    Page_Layer --> C_Side
    Core_Layer --> Infra_Layer
```

---

## 2. Decoupled Layer Architecture

### Layer 1: Test Suites (`tests/`)
- Contains test functions parameterized with fixtures and scoped with descriptive markers (`smoke`, `regression`, `negative`, `workflow`).
- Pure test logic: asserts expected business conditions, validates HTTP/DOM outcomes, and leaves interaction mechanics to lower layers.
- Direct WebDriver calls are prohibited in test functions.

### Layer 2: Business Workflows (`src/hrm_automation/workflows/`)
- Expresses end-to-end business intent (e.g., `create_employee_and_verify()`, `provision_user()`, `login_as_admin()`).
- Coordinates transitions across multiple Page Objects, handling data extraction, state validation, and multi-step verification.

### Layer 3: Page Objects & Reusable Components (`src/hrm_automation/pages/` & `components/`)
- Encapsulates view-specific locators and atomic UI interactions.
- Reusable UI widgets that appear repeatedly across modules (custom Vue dropdowns `.oxd-select-wrapper`, tables `.oxd-table`, toast alerts `.oxd-toast`, sidebar `.oxd-sidepanel`) are abstracted into independent Component classes.

### Layer 4: Core Engine (`src/hrm_automation/core/`)
- **BasePage**: Encapsulates resilient interaction primitives (`click()`, `type_text()`, `get_text()`, `scroll_into_view()`) with automatic stale-element recovery and fallback handlers.
- **WaitManager**: Enforces explicit synchronization using `WebDriverWait` and custom expected conditions (`wait_for_spinner_to_disappear()`, `wait_for_clickable()`).
- **Exceptions**: Custom domain exceptions (`ElementNotFoundException`, `TimeoutException`, `WorkflowExecutionException`) preserving underlying diagnostic tracebacks.

### Layer 5: Infrastructure & Test Data (`src/hrm_automation/core/driver_factory.py`, `data/`)
- **DriverFactory**: Implements W3C compliant browser configuration, headless execution, security sandbox flags, and Selenium Manager automated driver binary resolution.
- **Data Factories**: `EmployeeFactory`, `UserFactory`, and `CandidateFactory` generate synthetic, collision-resistant records namespaced with pytest worker IDs and unique UUID segments.
