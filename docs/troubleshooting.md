# Troubleshooting & Operational Triage Guide

This guide assists engineers and CI triage specialists in diagnosing and resolving automation failures.

---

## 1. Quick Diagnostic Checklist
When a test fails, inspect the following generated artifacts:
1. **Diagnostic Screenshots**: `artifacts/screenshots/FAILED_{test_name}_{timestamp}.png`
2. **Execution Logs**: `logs/execution.log` (or `logs/worker_{worker_id}.log` if running in parallel)
3. **JUnit XML Report**: `reports/junit/test-results.xml`

---

## 2. Common Failure Modes and Remediations

### 2.1 `ElementNotFoundException` or `TimeoutException`
- **Symptom**: `Timed out waiting for visibility of element ('xpath', ...)`
- **Common Causes**:
  - The page was in the middle of an asynchronous Vue.js transition or network AJAX request.
  - The public demo was experiencing transient latency.
- **Triage**:
  - Check the failure screenshot. If a loading spinner (`.oxd-loading-spinner`) is visible, verify `wait_for_spinner_to_disappear()` is called before interacting.
  - Inspect whether the selector matches the current OrangeHRM DOM.
  - In `config/settings.py` or `.env`, increase `DEFAULT_TIMEOUT` from 15 to 20 seconds during peak hours.

### 2.2 `StaleElementReferenceException`
- **Symptom**: `Element is not attached to the page document`
- **Root Cause**: OrangeHRM dynamically re-renders table rows or form controls upon dropdown selection.
- **Triage**:
  - The `BasePage.click()` and `BasePage.type_text()` methods automatically retry stale elements up to 3 times with 0.3s backoff.
  - If a stale element error still escapes, ensure you are not saving WebElements in variables across page actions. Always query elements dynamically through `BasePage.find()` or locator tuples.

### 2.3 `ElementClickInterceptedException`
- **Symptom**: `Element <button ...> is not clickable at point (x, y). Other element would receive the click: <div class="oxd-toast">`
- **Root Cause**: A temporary floating toast notification or header banner overlay covers the button.
- **Triage**:
  - The `BasePage.click()` method automatically catches `ElementClickInterceptedException`, scrolls the element to the viewport center, and retries with direct action chains or JS click.

### 2.4 Duplicate Record Collisions
- **Symptom**: `Username already exists` or `Employee Id already exists`
- **Root Cause**: Another test worker or external demo user previously registered the identifier.
- **Triage**:
  - Always generate data using `EmployeeFactory.create()`, `UserFactory.create()`, or `CandidateFactory.create()`.
  - These factories inject worker IDs (`PYTEST_XDIST_WORKER`), session tokens, and timestamps to eliminate collision risks.

### 2.5 Public Demo Rate Limiting or Outages
- **Symptom**: Connection timed out, 502 Bad Gateway, or Cloudflare verification page.
- **Triage**:
  - OrangeHRM's public demo is an external shared resource. If down, run the suite against a local Docker container:
    ```bash
    ENVIRONMENT=local pytest -m smoke
    ```
