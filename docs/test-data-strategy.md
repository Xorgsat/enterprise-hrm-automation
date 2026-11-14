# Test Data Strategy & Dynamic Isolation

## 1. Principles of Test Data Engineering
1. **Zero Shared Mutable State**: Tests must never rely on data created by other tests or external users.
2. **Deterministic Synthetics**: Data is generated dynamically using `Faker` backed by cryptographically collision-resistant unique tokens.
3. **Worker Isolation**: In multi-process test execution (`pytest-xdist`), data models incorporate the worker ID (`gw0`, `gw1`) to guarantee namespace separation.
4. **Non-Destructive Operations**: On shared environments (such as the OrangeHRM demo), tests only create and modify their own records. Purging pre-existing organizational data is strictly banned.

---

## 2. Test Data Factory Matrix

### 2.1 `EmployeeFactory`
- **Output**: `EmployeeData` Pydantic model
- **Generated Fields**:
  - `first_name`: `Aut_{worker}_{token}` (e.g. `Aut_gw0_7f2a`)
  - `middle_name`: `Marie`
  - `last_name`: `Test_{timestamp}` (e.g. `Test_48219`)
  - `employee_id`: Numeric timestamp string with worker token (e.g. `482197`)
  - `nickname`, `other_id`, `driver_license_number`
- **Guarantees**:
  - Fits within OrangeHRM's 30-character name fields.
  - Generates unique Employee IDs preventing "Employee Id already exists" form errors.

### 2.2 `UserFactory`
- **Output**: `SystemUserData` Pydantic model
- **Generated Fields**:
  - `username`: `usr_{worker}_{token}_{timestamp}` (length 18-24 chars, valid format)
  - `password`: `P@ssw0rd_{token}!` (satisfies complexity rule: >=8 chars, uppercase, lowercase, digit, symbol)
  - `user_role`: `"Admin"` or `"ESS"`
  - `status`: `"Enabled"`

### 2.3 `CandidateFactory`
- **Output**: `CandidateData` Pydantic model
- **Generated Fields**:
  - `first_name`: `Cand_{worker}_{token}`
  - `last_name`: `Talent_{timestamp}`
  - `email`: `cand_{worker}_{token}_{timestamp}@example-qa.com` (valid RFC 5322 format)
  - `contact_number`: `+1555{timestamp:04d}`

### 2.4 `LeaveFactory`
- **Output**: `LeaveApplicationData` Pydantic model
- **Generated Fields**:
  - `from_date`: Dynamic future date calculated as `today + days_in_future`
  - `to_date`: Calculated as `from_date + duration_days - 1`
  - `leave_type`: `"US - Vacation"`
