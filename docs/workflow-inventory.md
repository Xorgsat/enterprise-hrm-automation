# Workflow Inventory: Enterprise Business Processes

This inventory details all validated end-to-end and modular business workflows supported by OrangeHRM OS 5.9, their preconditions, required inputs, and expected outcomes.

---

## 1. Authentication and Session Workflows

### WF-AUTH-01: Standard Administrator Login & Dashboard Landing
- **Actors**: System Administrator
- **Preconditions**: User credentials configured in environment settings.
- **Workflow Steps**:
  1. Navigate to `/web/index.php/auth/login`.
  2. Input valid `username` and `password`.
  3. Submit login form.
  4. Synchronize on URL transition to `/dashboard/index`.
  5. Verify user profile dropdown renders with valid employee name.
- **Expected Outcome**: Active session established; dashboard widgets accessible.

### WF-AUTH-02: Safe Session Termination (Logout)
- **Actors**: Authenticated User
- **Preconditions**: Active user session.
- **Workflow Steps**:
  1. Click on `.oxd-userdropdown-tab`.
  2. Select `Logout` menu option.
  3. Synchronize on redirection to `/auth/login`.
  4. Attempt browser backward navigation.
- **Expected Outcome**: Session cookie invalidated; backward navigation redirects back to login page.

---

## 2. Personnel Information Management (PIM) Workflows

### WF-PIM-01: Dynamic Employee Creation and Verification
- **Actors**: HR Manager / Admin
- **Preconditions**: Authenticated Admin session.
- **Workflow Steps**:
  1. Navigate to PIM module (`/pim/viewEmployeeList`).
  2. Click `Add` button -> navigates to `/pim/addEmployee`.
  3. Generate unique namespaced employee identity:
     - `First Name`: `Aut_W{worker}_{hash}`
     - `Last Name`: `Test_{uuid}`
  4. Capture auto-assigned or custom `Employee ID`.
  5. Click `Save`.
  6. Wait for success toast notification (`Success: Successfully Saved`).
  7. Verify automatic navigation to `/pim/viewPersonalDetails/empNumber/{id}`.
  8. Return to `/pim/viewEmployeeList` and search by unique Employee ID.
- **Expected Outcome**: Employee record appears in search table with exact identity details.

### WF-PIM-02: Employee Profile Modification & Persistence
- **Actors**: HR Admin
- **Preconditions**: Employee created with known ID.
- **Workflow Steps**:
  1. Search employee in PIM list and open record for edit.
  2. Modify personal details (e.g., Nickname or Other ID).
  3. Click `Save` on Personal Details form.
  4. Refresh page / re-navigate to verify persistence.
- **Expected Outcome**: Updated field values persist accurately.

---

## 3. User Administration Workflows

### WF-ADM-01: System User Provisioning Linked to Employee
- **Actors**: System Administrator
- **Preconditions**: Existing employee record in system.
- **Workflow Steps**:
  1. Navigate to Admin > User Management (`/admin/viewSystemUsers`).
  2. Click `Add` button.
  3. Select `User Role` (e.g., `ESS` or `Admin`).
  4. Type employee name prefix and select the matching autocomplete suggestion.
  5. Select `Status` (`Enabled`).
  6. Generate unique username (`user_{worker}_{timestamp}`).
  7. Enter compliant password meeting complexity requirements.
  8. Click `Save`.
  9. Filter system users table by the new username.
- **Expected Outcome**: Provisioned user appears with correct role, linked employee, and enabled status.

---

## 4. Leave Management Workflows

### WF-LEAVE-01: Leave Application & List Inspection
- **Actors**: Employee / HR Admin
- **Preconditions**: Authenticated session; available leave type.
- **Workflow Steps**:
  1. Navigate to Leave > Apply (`/leave/applyLeave`).
  2. Select active `Leave Type` from custom dropdown.
  3. Select `From Date` and `To Date` (e.g., future business days).
  4. Enter comments.
  5. Submit application.
  6. Navigate to Leave > Leave List (`/leave/viewLeaveList`).
  7. Search by employee name or date range.
- **Expected Outcome**: Leave request appears in list with status `Pending Approval` or `Scheduled`.

### WF-LEAVE-02: Admin Leave Approval / Rejection
- **Actors**: HR Admin / Supervisor
- **Preconditions**: Pending leave request in leave list.
- **Workflow Steps**:
  1. Search for pending leave in `/leave/viewLeaveList`.
  2. Locate record row and click `Approve` or `Reject` action button.
  3. Synchronize on toast notification and table row status update.
- **Expected Outcome**: Leave status transitions to `Scheduled` or `Rejected`.

---

## 5. Recruitment Workflows

### WF-REC-01: Candidate Pipeline Lifecycle
- **Actors**: Recruiter / HR Admin
- **Preconditions**: Active vacancies in system.
- **Workflow Steps**:
  1. Navigate to Recruitment > Candidates (`/recruitment/viewCandidates`).
  2. Click `Add` button (`/recruitment/addCandidate`).
  3. Enter unique candidate identity (`First Name`, `Last Name`, unique `Email`).
  4. Select vacancy if available.
  5. Click `Save`.
  6. Verify candidate profile view loads with current status `Application Initiated`.
  7. Click `Shortlist` button -> Add note -> Confirm.
  8. Verify status transitions to `Shortlisted`.
- **Expected Outcome**: Candidate progresses deterministically through recruitment stages.

---

## 6. End-to-End Multi-Module Enterprise Workflows

### E2E-01: Complete Employee Onboarding Journey
- Crosses: **PIM -> Admin -> Directory**
- Sequence: Create new employee -> Provision system user account linked to employee -> Verify employee profile appears in company Directory.

### E2E-02: Leave Request & Approval Lifecycle
- Crosses: **PIM -> Leave Apply -> Leave List -> Status Verification**
- Sequence: Identify/create employee -> Submit leave request -> View in Admin Leave List -> Approve request -> Confirm final status.

### E2E-03: Recruitment Candidate Onboarding Journey
- Crosses: **Recruitment -> Candidates -> Pipeline Progression**
- Sequence: Create candidate -> Verify candidate in search table -> Advance candidate to Shortlisted status.
