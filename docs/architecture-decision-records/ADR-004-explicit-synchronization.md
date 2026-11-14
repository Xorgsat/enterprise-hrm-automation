# ADR-004: Explicit Synchronization, Custom Wait Conditions, and Anti-Flakiness Strategy

## Status
Accepted

## Context
OrangeHRM OS 5.x is built on modern frontend asynchronous patterns (Vue.js / single-page architecture). DOM nodes are dynamically mounted and unmounted, animations occur on dropdown expansion, and backend AJAX calls populate tables and toast banners. Flaky tests occur when automation uses static sleeps (`time.sleep`) or naive implicit waits.

## Decision
1. **Zero Implicit Wait (`implicitly_wait = 0`)**: Implicit waits conflict with explicit waits in Selenium, causing unpredictable compounding delays. Implicit wait is strictly disabled.
2. **Strict Ban on Hardcoded `time.sleep`**: Arbitrary sleeps are banned in production test code.
3. **Centralized `WaitManager`**: All synchronization utilizes explicit `WebDriverWait` with clear `expected_conditions` (visibility, clickability, staleness, URL changes, text presence).
4. **Custom Expected Conditions**:
   - `element_has_stopped_moving`: Verifies animations or transitions have concluded.
   - `element_text_matches_pattern`: Regex matching for dynamic counters like `(1) Record Found`.
   - `spinner_invisibility`: Waits for `.oxd-form-loader` / loading spinners to disappear before interacting.
5. **Stale Element Reference Recovery**: The `BasePage` encapsulates safe re-querying with bounded retry logic (up to 3 attempts with 0.3s backoff) when handling DOM nodes re-rendered by Vue.js.
6. **No Blanket Test Retries**: Blanket reruns mask concurrency defects and race conditions. Any test retry mechanism must log detailed initial failure artifacts (screenshot, URL, HTML dump, stack trace) before retrying.

## Consequences
- **Positive**: Blazing fast and deterministic test execution, predictable wait durations, zero race conditions, high developer trust in test results.
- **Trade-offs**: Requires automation engineers to understand the exact asynchronous state transitions for each UI interaction.
