"""
Page Object for OrangeHRM Authentication / Login Screen.
Encapsulates login inputs, validation alerts, credential helpers, and page assertions.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Encapsulates the /web/index.php/auth/login interface."""

    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ALERT_BANNER = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    INPUT_ERROR_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-group__message")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".orangehrm-login-forgot-header")
    BRANDING_LOGO = (By.CSS_SELECTOR, ".orangehrm-login-branding")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.login_url = f"{settings.base_url}/web/index.php/auth/login"

    def navigate_to_login(self) -> "LoginPage":
        """Navigate to the login view and await readiness."""
        logger.info(f"Navigating to login page: {self.login_url}")
        self.open_url(self.login_url)
        self.wait.wait_for_visibility(self.USERNAME_INPUT)
        return self

    def is_on_login_page(self) -> bool:
        """Check if browser is currently on the login page."""
        return "/auth/login" in self.current_url and self.is_visible(self.USERNAME_INPUT)

    def enter_username(self, username: str) -> "LoginPage":
        """Type username into the username field."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Type password into the password field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        """Submit the login form."""
        logger.debug("Clicking Login submit button.")
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str | None = None, password: str | None = None) -> None:
        """Complete credential entry and form submission."""
        logger.info(f"Executing login attempt for user: '{username}'")
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()

    def get_alert_error(self, timeout: int = 5) -> str:
        """Retrieve top alert banner message (e.g. 'Invalid credentials')."""
        return self.get_text(self.ALERT_BANNER, timeout=timeout)

    def get_field_errors(self) -> list[str]:
        """Retrieve all currently visible inline form error messages (e.g. ['Required'])."""
        elements = self.find_all(self.INPUT_ERROR_MESSAGES)
        return [e.text.strip() for e in elements if e.text.strip()]
