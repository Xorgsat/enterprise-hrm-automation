# Test Strategy: Enterprise HRM Platform

## 1. Scope and Mission
The primary objective of this quality engineering platform is to validate critical human resource operational flows on OrangeHRM Open Source (Starter Edition v5.9). Coverage balances positive business journeys, negative boundary enforcement, and cross-module workflow verifications.

---

## 2. Test Classification and Pyramid

```text
               ▲
              / \
             /   \     End-to-End Enterprise Workflows (3 Workflows)
            /     \    - Onboarding (PIM -> Admin -> Directory)
           / E2E   \   - Candidate Pipeline (Recruitment)
          /─────────\  - Leave Request & Management
         /           \
        /  Functional \  Module Integration & Business Rules (25 Tests)
       /  & Negative   \ - Employee creation, search, details persistence
      /                 \- Form validation, duplicate rejection, boundaries
     /───────────────────\
    /                     \ Core Infrastructure & Smoke Gate (13 Tests)
   /      Smoke & Sanity   \- Authentication lifecycle, session termination
  /─────────────────────────\- Navigation health, configuration validation
```

---

## 3. Risk-Based Testing Matrix

| Risk Domain | Potential Failure Impact | Automated Mitigation | Test Identifier |
|---|---|---|---|
| **Session Boundary Leakage** | Critical: Unauthenticated user accesses confidential employee records | Session termination checks, protected URL redirect, cache verification | `AUTH-001`, `AUTH-008`, `AUTH-009` |
| **Employee Record Corruption** | High: Incorrect personal details, lost employee records | Synthetic employee generation, persistence verification across refreshes | `PIM-002`, `PIM-005`, `E2E-001` |
| **Recruitment Data Loss** | High: Candidate applications dropped or inaccessible | Full candidate lifecycle from submission to search verification | `REC-003`, `REC-004`, `E2E-002` |
| **Form Validation Bypass** | Medium: Malformed data entered into HR database | Comprehensive negative form validation suites | `AUTH-004`, `PIM-007`, `REC-009` |
| **Parallel Collision** | Medium: False test failures due to duplicate usernames/IDs | Dynamic namespacing using pytest-xdist worker tokens + UUIDs | All tests |

---

## 4. Execution Profiles

| Marker | Scope | Trigger | SLA Target |
|---|---|---|:---:|
| `@pytest.mark.smoke` | 12 critical path tests | Every Pull Request, PR merge, and Daily Cron | < 2 minutes |
| `@pytest.mark.regression` | Full 41 test scenarios | Nightly build, release candidate tag, manual dispatch | < 8 minutes (parallel) |
| `@pytest.mark.negative` | Validation errors, boundaries | PR validation & regression | < 3 minutes |
| `@pytest.mark.workflow` | Cross-module E2E journeys | Nightly build & release candidate tag | < 4 minutes |
