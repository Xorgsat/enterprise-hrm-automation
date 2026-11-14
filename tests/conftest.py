"""
Root Pytest Configuration and Test Fixtures.
Provides isolated browser lifecycles, failure hooks with automatic screenshots,
worker-aware logging, and authenticated session fixtures.
"""

import os
import uuid

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import FrameworkSettings, settings
from hrm_automation.core.driver_factory import DriverFactory
from hrm_automation.utilities.logging import configure_logging, get_logger
from hrm_automation.utilities.screenshots import capture_screenshot

logger = get_logger(__name__)


def pytest_configure(config):
    """Initialize logging and worker namespaces before test run starts."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    configure_logging(level=settings.log_level, worker_id=worker_id)
    logger.info(f"Pytest run initialized on worker '{worker_id}' | Target: {settings.base_url}")


@pytest.fixture(scope="session")
def env_settings() -> FrameworkSettings:
    """Session-scoped framework configuration."""
    return settings


@pytest.fixture(scope="session")
def test_session_id() -> str:
    """Generate a unique run ID for the entire test session."""
    return uuid.uuid4().hex[:6]


@pytest.fixture(scope="function")
def test_namespace(request, test_session_id) -> str:
    """Generate a collision-resistant namespace for test data created in this test."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "m")
    unique_suffix = uuid.uuid4().hex[:4]
    return f"{worker_id}_{test_session_id}_{unique_suffix}"


@pytest.fixture(scope="function")
def driver(request, env_settings):
    """
    Function-scoped isolated WebDriver instance.
    Guarantees browser isolation for every individual test.
    Automatically captures screenshot on test failure.
    """
    logger.info(f"Starting browser session for test: '{request.node.name}'")
    web_driver = DriverFactory.create_driver(config=env_settings)

    # Store driver on test node so pytest hooks can access it for failure diagnostics
    request.node.driver = web_driver

    yield web_driver

    # Teardown
    logger.info(f"Closing browser session for test: '{request.node.name}'")
    DriverFactory.quit_driver(web_driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook executed after each test phase (setup, call, teardown).
    Detects failures and captures immediate visual and diagnostic evidence.
    """
    outcome = yield
    report = outcome.get_result()

    # We only care about failures during the call phase
    if report.when == "call" and report.failed:
        web_driver: WebDriver = getattr(item, "driver", None)
        if web_driver and settings.screenshot_on_failure:
            test_name = item.name
            logger.warning(f"Test '{test_name}' failed at URL: {web_driver.current_url}")
            screenshot_path = capture_screenshot(
                driver=web_driver,
                name=f"FAILED_{test_name}",
                attach_to_allure=True,
            )
            if screenshot_path:
                logger.info(f"Failure screenshot archived at: {screenshot_path}")


@pytest.fixture(scope="function")
def authenticated_driver(driver, env_settings):
    """
    Convenience fixture providing a pre-authenticated Admin session on the Dashboard.
    Uses proper UI login workflow (no fragile session hacking).
    """
    from hrm_automation.pages.auth.login_page import LoginPage
    from hrm_automation.pages.dashboard.dashboard_page import DashboardPage

    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(
        username=env_settings.admin_username,
        password=env_settings.admin_password,
    )
    dashboard_page = DashboardPage(driver)
    dashboard_page.verify_is_displayed(timeout=25)
    return driver
