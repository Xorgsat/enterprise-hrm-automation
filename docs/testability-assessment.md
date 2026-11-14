# Testability Assessment: OrangeHRM Open Source (v5.9)

## 1. Executive Summary
OrangeHRM OS 5.9 demonstrates good UI-level testability with structured CSS class naming conventions (`oxd-*`), clear form inputs, consistent toast alerts, and deterministic URL routing. However, testability is constrained on the public demo due to shared-state volatility, lack of backend access, and absence of dedicated `data-testid` attributes.

---

## 2. Testability Evaluation Grid

| Quality Dimension | Score (1-5) | Analysis & Observations | Automation Strategy |
|---|:---:|---|---|
| **Controllability** | 3.5 / 5 | Can control system state via UI forms. No direct database or API backdoor on public demo. | Self-contained UI setup steps with namespaced test entities. |
| **Observability** | 4.0 / 5 | Clear URL routing changes, predictable toast notifications (`.oxd-toast`), distinct validation error messages (`.oxd-input-group__message`). | Explicit synchronization on toasts, URLs, and row count indicators. |
| **Isolability** | 3.0 / 5 | Shared demo environment means other users share the same database. | Rigorous namespacing via `Faker` + worker IDs; test isolation. |
| **Simplicity** | 4.5 / 5 | Standard business workflows (CRUD on employees, users, leave, candidates). | Clean Page Object Model and Workflow Service abstractions. |
| **Stability** | 3.5 / 5 | Public demo experiences intermittent latency or external resets. Self-hosted instances provide 5/5 stability. | Robust timeouts (15s default), zero implicit wait, retry on stale elements. |

---

## 3. Locator Stability Ranking
To ensure longevity and maintainability across minor application updates, locators follow this strict hierarchy:

1. **Standard Named Inputs**: `name="username"`, `name="password"`, `name="firstName"`, `name="lastName"` (Most stable).
2. **Semantic Form Group / Labels**: `//label[text()='User Role']/../following-sibling::div//div[contains(@class, 'oxd-select-text')]`.
3. **Structured Component Classes**: `.oxd-table`, `.oxd-toast`, `.oxd-sidepanel`, `.oxd-userdropdown-tab`.
4. **Action Buttons by Role / Type**: `button[type='submit']`, `button:has-text('Save')`, `button:has-text('Add')`.
5. **CSS Scoped Hierarchy**: `.oxd-table-body .oxd-table-card:first-child .oxd-table-cell:nth-child(2)`.
6. **Prohibited Selectors**: Absolute XPath (`/html/body/...`), arbitrary index paths without contextual parents, fragile generated CSS hashes.

---

## 4. Test Environment Matrix

| Tier | Environment | Target Usage | Concurrency | Destructive Tests |
|---|---|---|:---:|:---:|
| **Tier 1** | Local / Docker Self-Hosted | Development, Full Regression, PR Gates | 2-4 Workers | Permitted |
| **Tier 2** | Public Hosted Demo | Smoke Verification, Showcase Demos | 1-2 Workers | Strictly Prohibited |
| **Tier 3** | Enterprise Staging | Release Candidate Verification | 2-4 Workers | Permitted |
