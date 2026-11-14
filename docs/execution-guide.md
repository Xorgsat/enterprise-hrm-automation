# Test Execution & CLI Guide

This guide covers all test execution commands, parallel concurrency options, marker filtering, and report generation.

---

## 1. Fast Smoke Verification
Run business-critical smoke tests across all modules:
```bash
pytest -m smoke -v
```
Or use the convenience helper script:
```bash
python scripts/run_smoke.py
```

---

## 2. Module-Specific Test Execution

### Authentication & Session Lifecycle
```bash
pytest tests/authentication/ -v
# Or by marker
pytest -m authentication -v
```

### Personnel Information Management (PIM)
```bash
pytest tests/pim/ -v
# Or by marker
pytest -m pim -v
```

### Admin & User Management
```bash
pytest tests/admin/ -v
# Or by marker
pytest -m admin -v
```

### Leave Management
```bash
pytest tests/leave/ -v
# Or by marker
pytest -m leave -v
```

### Recruitment Pipeline
```bash
pytest tests/recruitment/ -v
# Or by marker
pytest -m recruitment -v
```

### Employee Self-Service & Directory
```bash
pytest tests/self_service/ -v
# Or by marker
pytest -m self_service -v
```

### Multi-Module Enterprise End-to-End Workflows
```bash
pytest tests/workflows/ -v
# Or by marker
pytest -m workflow -v
```

---

## 3. Negative Testing & Boundary Validation
Execute all negative scenarios testing form validations and error banners:
```bash
pytest -m negative -v
```

---

## 4. Parallel Execution (`pytest-xdist`)
Leverage worker isolation to run tests concurrently:
```bash
# Run with 2 workers (recommended for public demo to prevent rate limiting)
pytest -n 2 -v

# Run with 4 workers (recommended for local Docker self-hosted instance)
pytest -n 4 -v
```

---

## 5. Visual Headed Execution
For local debugging with visible browser windows:
In `.env`, set:
```ini
HEADLESS=false
```
Or run directly:
```bash
HEADLESS=false pytest tests/authentication/test_authentication.py -k "test_auth_001"
```

---

## 6. Report Generation

### JUnit XML Reports
Generated automatically in `reports/junit/test-results.xml` on every run.

### Allure Visual Dashboard
To generate and view interactive Allure HTML reports:
```bash
# Ensure allure CLI is installed (e.g. brew install allure)
allure serve reports/allure-results
```

---

## 7. Artifact Cleaning
Clear previous logs, screenshots, and Allure results:
```bash
python scripts/clean_test_artifacts.py
```
