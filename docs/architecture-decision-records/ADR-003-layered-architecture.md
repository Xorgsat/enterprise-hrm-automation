# ADR-003: Layered Automation Architecture

## Status
Accepted

## Context
A frequent anti-pattern in browser test automation is conflating page interaction mechanics, business workflow orchestration, assertion logic, and infrastructure setup in monolithic test scripts. This leads to high maintenance costs, fragile tests, and poor readability.

## Decision
We enforce a strict 5-layer decoupled architectural hierarchy:

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Test Suites (pytest test functions & markers)  │
│ - Only high-level assertions and business verification  │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Layer 2: Business Workflows (Service Orchestrators)     │
│ - Orchestrates multi-page business journeys             │
│ - e.g., EmployeeManagementWorkflow, LeaveWorkflow       │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Layer 3: Page Objects & UI Components                   │
│ - Encapsulates locators and user actions per view       │
│ - Reusable Components: DataTable, Dropdown, Modal, Toast│
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Layer 4: Core Engine & Synchronization (BasePage & Wait)│
│ - Explicit wait conditions, retry stale element handlers│
│ - Standardized interaction methods (click, type, scroll)│
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Layer 5: Infrastructure & Driver Factory                │
│ - WebDriver lifecycle, environment settings, fixtures   │
└─────────────────────────────────────────────────────────┘
```

### Architectural Guardrails
1. **No Selenium in Tests**: Test files (`test_*.py`) must never import or call `webdriver` methods directly.
2. **No Assertions in Page Objects**: Page objects return state (strings, booleans, objects) or trigger transitions; assertions belong in test functions or workflow validators.
3. **Component Reusability**: Common OrangeHRM elements (the custom dropdown `.oxd-select-wrapper`, tables `.oxd-table`, toast banners `.oxd-toast`) are abstracted into standalone `Component` classes.

## Consequences
- **Positive**: High maintainability, clear separation of concerns, rapid defect localization, reusable business workflows across multiple test scenarios.
- **Trade-offs**: Requires disciplined adherence to architectural boundaries and slightly more initial boilerplate classes.
