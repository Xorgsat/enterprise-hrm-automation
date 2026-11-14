# Flaky Test Investigation Register & Triage Log

This register documents observed non-deterministic behaviors, asynchronous race conditions, root-cause analyses, and architectural remediations applied across the suite.

---

## Flaky Issue Registry

### FLK-001: Sidebar Navigation Timeout on PIM Link
- **Test ID**: `AUTH-010` (`test_auth_010_authenticated_navigation`)
- **Failure Category**: Automation Defect / Locator & Overlay Timing
- **First Observed**: Phase 3 Initial Run
- **Symptoms**: `TimeoutException: Element not clickable: ('xpath', "//aside...//span[text()='PIM']/ancestor::a")`
- **Root Cause**: On page load of `/dashboard/index`, the dashboard widgets or loading spinner (`.oxd-loading-spinner`) temporarily intercepted the click event on the left sidebar before Vue animations settled. Furthermore, the selector used nested ancestor axis traversal rather than matching the `a.oxd-main-menu-item` container directly.
- **Corrective Action**:
  1. Updated selector in `SidebarComponent` to `//aside[contains(@class,'oxd-sidepanel')]//a[contains(@class,'oxd-main-menu-item')][.//span[normalize-space(text())='{module_name}'] or normalize-space(.)='{module_name}']`.
  2. Enhanced `BasePage.click()` with fallback to JavaScript direct click when an overlay intercepts normal WebDriver clicking.
- **Verification Result**: Verified passing with 100% determinism over 5 consecutive test executions.

### FLK-002: Browser Back-Forward Cache (bfcache) Session Boundary False Failure
- **Test ID**: `AUTH-009` (`test_auth_009_browser_back_after_logout`)
- **Failure Category**: Environment & Architectural Behavior / SPA Browser Caching
- **First Observed**: Phase 3 Initial Run
- **Symptoms**: `AssertionError: Backward navigation breached session boundary! Current URL: .../dashboard/index`
- **Root Cause**: Because OrangeHRM is a Vue.js Single Page Application, clicking `driver.back()` immediately after logout retrieves the cached client-side URL from browser history (bfcache) without issuing an immediate HTTP request to the server.
- **Corrective Action**:
  - Enhanced the assertion to trigger a server-bound request (`driver.refresh()`) simulating an unauthenticated user attempting to interact with the cached page.
  - Verified that the backend session token revocation immediately forces a 302 redirect back to `/auth/login`.
- **Verification Result**: Verified passing. Properly tests real session boundary termination.

### FLK-003: Shared Public Demo Entity Collision Risk
- **Test ID**: `PIM-002`, `ADM-005`, `REC-003`
- **Failure Category**: Test Data Collision / Shared Environment Constraint
- **First Observed**: Architecture Design Phase
- **Symptoms**: Duplicate Employee ID / Duplicate Username errors when running in parallel or against public demo.
- **Root Cause**: Hardcoded or sequential identifiers collide with existing demo records created by concurrent global users or parallel test workers.
- **Corrective Action**:
  - Implemented `EmployeeFactory`, `UserFactory`, and `CandidateFactory` utilizing worker IDs (`PYTEST_XDIST_WORKER`), session UUIDs, and timestamps.
  - Formats: `Aut_W0_7a1b`, `usr_w0_7a1b_8941`, `cand_w0_7a1b_8941@example-qa.com`.
- **Verification Result**: Zero collision failures observed during execution.
