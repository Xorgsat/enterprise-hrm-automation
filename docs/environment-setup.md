# Environment Setup Guide

This guide details the prerequisites and instructions to configure the test automation platform on macOS, Linux, and Windows.

---

## 1. System Prerequisites
- **Python**: Version `3.10` or higher (Python 3.12 recommended).
- **Google Chrome**: Stable version (version 120+).
- **Git**: Installed and configured.
- **Package Manager**: Standard `pip` or modern `uv`.

> [!NOTE]
> WebDriver binaries (ChromeDriver) are managed automatically by Selenium 4's built-in **Selenium Manager**. No manual `chromedriver` download or path export is required.

---

## 2. Quickstart Installation (Recommended: `uv`)

```bash
# 1. Clone repository
git clone https://github.com/your-username/enterprise-hrm-automation.git
cd enterprise-hrm-automation

# 2. Create Python 3.12 virtual environment
uv venv .venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install pinned dependencies
uv pip install -r requirements.txt
```

---

## 3. Alternative Installation (Standard `pip`)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Configuration Setup
Copy the template configuration file:
```bash
cp .env.example .env
```

Review and adjust variables in `.env`:
```ini
BASE_URL=https://opensource-demo.orangehrmlive.com
ENVIRONMENT=demo
ADMIN_USERNAME=Admin
ADMIN_PASSWORD=admin123
BROWSER=chrome
HEADLESS=true
DEFAULT_TIMEOUT=15
WORKERS=2
LOG_LEVEL=INFO
```

---

## 5. Verify Setup
Run the infrastructure smoke check to ensure browser launch and reachability:
```bash
pytest tests/smoke/test_infrastructure.py -v
```
Expected output:
```text
tests/smoke/test_infrastructure.py::TestInfrastructure::test_configuration_loading PASSED
tests/smoke/test_infrastructure.py::TestInfrastructure::test_browser_lifecycle_and_navigation PASSED
tests/smoke/test_infrastructure.py::TestInfrastructure::test_screenshot_capture_utility PASSED
3 passed in ~12s
```
