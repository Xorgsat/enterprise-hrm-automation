# Application Discovery Document: OrangeHRM Open Source (v5.9)

## 1. Overview and Environment Profile
- **Target Application**: OrangeHRM Open Source Starter Edition
- **Live Version Verified**: `OrangeHRM OS 5.9 | © 2005 - 2026 OrangeHRM, Inc.`
- **Target URL**: `https://opensource-demo.orangehrmlive.com`
- **Hosting Environment**: Nginx on Ubuntu Linux, PHP 8.x backend with MySQL, Vue.js-based frontend SPA architecture.
- **Account Under Test**: Administrator (`Admin` / `admin123`)

---

## 2. Global Navigation & Architecture
The application features a responsive sidebar (`.oxd-sidepanel`), top bar header (`.oxd-topbar-header`), sub-navigation tabs (`.oxd-topbar-body-nav-tab`), and an avatar dropdown (`.oxd-userdropdown-tab`).

### Discovered Navigation Endpoints
| Module | Destination URL | Primary Status |
|---|---|---|
| **Login** | `/web/index.php/auth/login` | Active / Verified |
| **Dashboard** | `/web/index.php/dashboard/index` | Active / Verified |
| **Admin** | `/web/index.php/admin/viewSystemUsers` | Active / Verified |
| **PIM** | `/web/index.php/pim/viewEmployeeList` | Active / Verified |
| **Leave** | `/web/index.php/leave/viewLeaveList` | Active / Verified |
| **Time** | `/web/index.php/time/viewTimeModule` | Active / Secondary |
| **Recruitment** | `/web/index.php/recruitment/viewCandidates` | Active / Verified |
| **My Info** | `/web/index.php/pim/viewPersonalDetails/empNumber/{id}` | Active / Verified |
| **Performance**| `/web/index.php/performance/viewPerformanceModule` | Active / Secondary |
| **Directory** | `/web/index.php/directory/viewDirectory` | Active / Verified |
| **Maintenance**| `/web/index.php/maintenance/viewMaintenanceModule` | Requires sudo/admin password |
| **Claim** | `/web/index.php/claim/viewClaimModule` | Active / Secondary |
| **Buzz** | `/web/index.php/buzz/viewBuzz` | Social Feed |

---

## 3. Discovered Module Records

### 3.1 Authentication & Session
- **Availability**: Accessible
- **User Role**: Admin / Any System User
- **Entry Point**: `/web/index.php/auth/login`
- **Primary Workflow**: Form submission with credentials, credential verification, JWT/PHP session establishment, redirect to `/dashboard/index`.
- **Required Fields**: `Username`, `Password`
- **Optional Fields**: None
- **Observed Validation**:
  - Missing field: Inline error `.oxd-input-group__message` reading `"Required"`.
  - Invalid credentials: Top toast alert `.oxd-alert-content-text` reading `"Invalid credentials"`.
- **State Changes**: Redirect to `/dashboard/index` on success; stay on `/auth/login` on failure.
- **Testability**: Highly Automatable.
- **Limitations**: Rate-limiting or temporary cloud flare protections on excessive brute-force attempts.

### 3.2 Admin (System User Management)
- **Availability**: Accessible
- **User Role**: Admin
- **Entry Point**: `/web/index.php/admin/viewSystemUsers`
- **Primary Workflow**: Filter existing system users, create system users with roles (Admin / ESS), employee name linkage, and credentials.
- **Required Fields**: `User Role`, `Employee Name`, `Status`, `Username`, `Password`, `Confirm Password`.
- **Optional Fields**: None in creation modal.
- **Observed Validation**:
  - Username uniqueness check (asynchronous check shows error if duplicate).
  - Employee autocomplete requires selecting an existing employee from popup dropdown.
  - Password strength validation: Minimum 8 characters, number, lowercase, uppercase.
- **State Changes**: New record in `.oxd-table`, success toast notification (`Success: Successfully Saved`).
- **Testability**: Highly Automatable.
- **Limitations**: Shared public demo environment contains arbitrary users created by other testers; requires unique username prefixing.

### 3.3 PIM (Personnel Information Management)
- **Availability**: Accessible
- **User Role**: Admin
- **Entry Point**: `/web/index.php/pim/viewEmployeeList` and `/web/index.php/pim/addEmployee`
- **Primary Workflow**: Add employee, capture auto-generated or custom employee ID, toggle "Create Login Details", search and filter employees, view/modify personal and contact details.
- **Required Fields**: `First Name`, `Last Name`.
- **Optional Fields**: `Middle Name`, `Employee Id`, `Photograph`, `Create Login Details` toggle.
- **Observed Validation**:
  - Missing first/last name triggers `"Required"`.
  - Duplicate employee ID triggers `"Employee Id already exists"`.
- **State Changes**: Redirects to personal details page (`/pim/viewPersonalDetails/empNumber/<id>`), row appears in PIM employee table.
- **Testability**: Highly Automatable.
- **Limitations**: Do not delete existing employee records; use namespaced unique names.

### 3.4 Leave Management
- **Availability**: Accessible
- **User Role**: Admin / ESS
- **Entry Point**: `/web/index.php/leave/viewLeaveList` and `/web/index.php/leave/applyLeave`
- **Primary Workflow**: Apply for leave (selecting Leave Type, From Date, To Date, Comments), list submitted leave requests, Admin approve/reject/cancel requests.
- **Required Fields**: `Leave Type`, `From Date`, `To Date`.
- **Optional Fields**: `Partial Days`, `Duration`, `Comments`.
- **Observed Validation**:
  - Missing leave type / dates triggers `"Required"`.
  - Date ordering: "To date should be after from date".
  - Entitlement check: Warns if balance is 0 or insufficient.
- **State Changes**: Status changes between `Pending Approval`, `Scheduled`, `Taken`, `Rejected`, `Cancelled`.
- **Testability**: Highly Automatable.
- **Limitations**: Employee must have entitlement configured to apply for specific leave types without zero-balance warnings.

### 3.5 Recruitment
- **Availability**: Accessible
- **User Role**: Admin / Hiring Manager
- **Entry Point**: `/web/index.php/recruitment/viewCandidates` and `/web/index.php/recruitment/addCandidate`
- **Primary Workflow**: Add candidate, assign vacancy, record contact details, advance candidate status through workflow stages (`Shortlist`, `Schedule Interview`, `Mark Interview Passed`, `Offer Job`, `Hire`, `Reject`).
- **Required Fields**: `First Name`, `Last Name`, `Email`.
- **Optional Fields**: `Middle Name`, `Vacancy`, `Contact Number`, `Resume`, `Keywords`, `Date of Application`, `Notes`, `Consent to keep data`.
- **Observed Validation**:
  - Email format validation (`"Expected format: admin@example.com"`).
  - Required field indicators.
- **State Changes**: Progression of stage action buttons (`Shortlist` -> `Schedule Interview` -> `Offer Job`), candidate table status updates.
- **Testability**: Highly Automatable.
- **Limitations**: Modifying or advancing another tester's candidate might cause transient state conflicts; create dedicated candidate per test.

### 3.6 My Info (Employee Self-Service)
- **Availability**: Accessible
- **User Role**: Logged-in User (Admin or ESS)
- **Entry Point**: `/web/index.php/pim/viewPersonalDetails/empNumber/7`
- **Primary Workflow**: View personal details, update Nickname, Driver's License, Other ID, Nationality, Marital Status, save changes.
- **Required Fields**: First Name, Last Name.
- **Optional Fields**: Nickname, Other ID, License Number, Expiry Date, SSN, SIN, Nationality, Marital Status, DOB, Gender.
- **Observed Validation**: Save trigger prompts toast `Successfully Saved`.
- **State Changes**: Persistent update on record.
- **Testability**: Automatable.
- **Limitations**: In public demo, editing the shared default Admin's personal information may be overwritten by other demo users. Tests must isolate edited fields and verify immediate persistence.

### 3.7 Directory
- **Availability**: Accessible
- **User Role**: All authenticated users
- **Entry Point**: `/web/index.php/directory/viewDirectory`
- **Primary Workflow**: Search employee directory by Name, Job Title, or Location; view directory profile cards.
- **Required Fields**: None (search filters are optional).
- **Observed Validation**: Autocomplete matching.
- **State Changes**: Directory cards render matching employee profiles.
- **Testability**: Automatable (read-only verification).

---

## 4. UI Component Anatomy & Locators

### 4.1 Custom Select Dropdown
- **DOM Container**: `.oxd-select-wrapper`
- **Trigger Element**: `.oxd-select-text`
- **Options Container**: `.oxd-select-dropdown`
- **Option Item**: `.oxd-select-option`
- **Interaction Rule**: Normal `<select>` APIs (`Select(elem)`) do **not** work. The automation must click the wrapper, wait for `.oxd-select-dropdown` to be visible, then click the target `.oxd-select-option[role='option']` matching desired text.

### 4.2 Data Table
- **Container**: `.oxd-table`
- **Header Row**: `.oxd-table-header`
- **Header Columns**: `.oxd-table-th`
- **Body**: `.oxd-table-body`
- **Data Rows**: `.oxd-table-card` or `.oxd-table-row`
- **Cells**: `.oxd-table-cell`
- **Row Actions**: Action buttons (Edit, Delete, Approve, Reject) located in the trailing cell (`.oxd-table-cell-actions`).

### 4.3 Form Inputs and Date Pickers
- **Text Inputs**: `input.oxd-input`
- **Date Picker Wrapper**: `.oxd-date-input`
- **Date Input**: `.oxd-date-input input`
- **Toast Notifications**: `.oxd-toast`, `.oxd-toast-content-text`
- **Validation Messages**: `.oxd-input-group__message`
- **Loading Overlay**: `.oxd-form-loader`
