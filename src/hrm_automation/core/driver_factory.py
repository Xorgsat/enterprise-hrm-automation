"""
WebDriver Factory and Lifecycle Management.
Instantiates and configures browser drivers using Selenium Manager and W3C compliant options.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import FrameworkSettings, settings
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class DriverFactory:
    """Factory for creating and configuring isolated WebDriver sessions."""

    @staticmethod
    def create_driver(
        headless: bool | None = None,
        browser: str | None = None,
        config: FrameworkSettings | None = None,
    ) -> WebDriver:
        """Create and return a configured WebDriver instance based on framework settings."""
        cfg = config or settings
        browser_name = (browser or cfg.browser).lower()
        is_headless = headless if headless is not None else cfg.headless

        logger.info(
            f"Initializing WebDriver: browser='{browser_name}', headless={is_headless}, "
            f"target='{cfg.base_url}'"
        )

        if browser_name == "chrome":
            options = ChromeOptions()
            if is_headless:
                options.add_argument("--headless=new")

            # Production-grade flags for container and headless stability
            options.add_argument(f"--window-size={cfg.window_width},{cfg.window_height}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            options.add_argument("--remote-allow-origins=*")
            options.add_argument("--ignore-certificate-errors")

            # Anti-automation detection mitigation (prevents standard bot flags)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            # Leverage Selenium 4 built-in Selenium Manager
            driver = webdriver.Chrome(options=options)
        else:
            raise ValueError(
                f"Unsupported browser: '{browser_name}'. Only 'chrome' is currently configured."
            )

        # Zero implicit wait policy (ADR-004)
        driver.implicitly_wait(cfg.implicit_wait)
        driver.set_page_load_timeout(cfg.page_load_timeout)

        logger.info(f"WebDriver successfully initialized [Session ID: {driver.session_id}]")
        return driver

    @staticmethod
    def quit_driver(driver: WebDriver | None) -> None:
        """Safely terminate WebDriver session."""
        if driver:
            try:
                session_id = driver.session_id
                driver.quit()
                logger.info(f"WebDriver session {session_id} cleanly terminated.")
            except Exception as e:
                logger.warning(f"Error encountered while terminating WebDriver session: {e}")
