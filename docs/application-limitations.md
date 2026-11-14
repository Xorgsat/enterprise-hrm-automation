# Application Limitations & Environment Constraints

## 1. Public Hosted Demo Environment Constraints
Target URL: `https://opensource-demo.orangehrmlive.com`

The public demonstration instance is a globally shared, volatile environment used simultaneously by multiple automated suites, recruiters, and learners worldwide.

### 1.1 Non-Destructive Operations Requirement
- **Hard Restriction**: Automated tests must **never** execute bulk deletions, purge existing organizational entities, or delete pre-existing system accounts (`Admin`, default employees, default leave configurations).
- **Ethical & Legal Compliance**: As documented in the OrangeHRM Vulnerability Disclosure Policy, security testing, fuzzing, brute-forcing, and high-frequency denial-of-service style loads are strictly prohibited against hosted demo infrastructure.

### 1.2 Data Volatility & Periodic Reset
- The public demo environment undergoes unannounced periodic resets (wiping recently created custom users/employees).
- **Automation Rule**: Tests must **never** assume that data created in an earlier test execution persists to a later execution. Every test suite must dynamically provision its own records within its execution scope.

### 1.3 Concurrency & Collision Risks
- If multiple tests or parallel workers create users with common names like `johndoe` or `testuser`, collisions will immediately cause test failures.
- **Remediation**: All dynamic test data utilizes unique namespacing including worker process ID, timestamp, and UUID segments.

---

## 2. OrangeHRM Open Source Starter Edition Functional Limitations
The Open Source Starter edition differs from the Enterprise Commercial edition in several key operational areas:

| Capability | Starter Edition (Demo) | Enterprise Edition | Automation Impact |
|---|---|---|---|
| **Multi-Level Approval Chains** | Single-tier approval | Multi-tier matrix workflows | Approval tests must test single-tier supervisor/admin sign-off |
| **REST API Direct Endpoints** | Restricted/Closed on public demo | Full OAuth2 REST API | Public demo tests must execute via UI; API shortcuts only on private instances |
| **Direct Database Access** | No SQL access | Available in self-hosted | Assertions must rely on UI feedback and state rather than SQL queries |
| **Granular Custom Roles** | Basic Admin vs ESS | Custom RBAC role designer | Role-based authorization tests are bounded by Admin and ESS capabilities |
| **Email Server / SMTP** | Disabled / Mocked on demo | Live SMTP Integration | Email verification must not be asserted as an external network call on demo |
| **Leave Entitlements & Balances** | Default `Admin` account has zero assigned leave balance | Configurable per employee/year | Leave submission and form negative validation on `/leave/applyLeave` are blocked by "No Leave Types with Leave Balance" on the demo; requires self-hosted instance with assigned entitlements |

---

## 3. Browser & DOM Synchronization Characteristics
1. **Vue.js Virtual DOM Rendering**: Element nodes are frequently detached and re-attached when forms switch tabs or filters are applied. Selenium tests must use explicit expected conditions and stale-element recovery.
2. **Custom Select Dropdown**: The application does not use native `<select>` tags; standard Selenium `Select` class throws `UnexpectedTagNameException`. All dropdowns require component-level interaction via `.oxd-select-wrapper` and `.oxd-select-option`.
3. **Floating Toast Notifications**: Toast banners (`.oxd-toast`) auto-dismiss after approximately 4 seconds. Verification must catch the toast before it unmounts or verify the underlying persistent table row state.
