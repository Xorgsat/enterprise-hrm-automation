"""
Centralized Synchronization and Explicit Wait Management.
Encapsulates WebDriverWait and custom expected conditions for asynchronous UI state transitions.
"""

import time

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.common.exceptions import (
    TimeoutException as SeleniumTimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from hrm_automation.core.exceptions import TimeoutException
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class WaitManager:
    """Explicit wait synchronization engine."""

    def __init__(self, driver: WebDriver, default_timeout: int = 15):
        self.driver = driver
        self.default_timeout = default_timeout

    def _get_wait(self, timeout: int = None, poll_frequency: float = 0.3) -> WebDriverWait:
        t = timeout if timeout is not None else self.default_timeout
        return WebDriverWait(
            self.driver,
            timeout=t,
            poll_frequency=poll_frequency,
            ignored_exceptions=[NoSuchElementException, StaleElementReferenceException],
        )

    def wait_for_visibility(
        self, locator: tuple[By, str], timeout: int = None, error_message: str = ""
    ) -> WebElement:
        """Wait until an element is visible in the DOM."""
        try:
            return self._get_wait(timeout).until(
                EC.visibility_of_element_located(locator),
                message=error_message or f"Element not visible: {locator}",
            )
        except SeleniumTimeoutException as e:
            raise TimeoutException(
                f"Timed out waiting for visibility of element {locator}. {error_message}", e
            ) from e

    def wait_for_presence(
        self, locator: tuple[By, str], timeout: int = None, error_message: str = ""
    ) -> WebElement:
        """Wait until an element is present in the DOM."""
        try:
            return self._get_wait(timeout).until(
                EC.presence_of_element_located(locator),
                message=error_message or f"Element not present in DOM: {locator}",
            )
        except SeleniumTimeoutException as e:
            raise TimeoutException(
                f"Timed out waiting for presence of element {locator}. {error_message}", e
            ) from e

    def wait_for_clickable(
        self, locator: tuple[By, str], timeout: int = None, error_message: str = ""
    ) -> WebElement:
        """Wait until an element is visible and enabled for interaction."""
        try:
            return self._get_wait(timeout).until(
                EC.element_to_be_clickable(locator),
                message=error_message or f"Element not clickable: {locator}",
            )
        except SeleniumTimeoutException as e:
            raise TimeoutException(
                f"Timed out waiting for element {locator} to become clickable. {error_message}", e
            ) from e

    def wait_for_invisibility(
        self, locator: tuple[By, str], timeout: int = None, error_message: str = ""
    ) -> bool:
        """Wait until an element is invisible or detached from the DOM."""
        try:
            return self._get_wait(timeout).until(
                EC.invisibility_of_element_located(locator),
                message=error_message or f"Element still visible: {locator}",
            )
        except SeleniumTimeoutException as e:
            raise TimeoutException(
                f"Timed out waiting for element {locator} to become invisible. {error_message}", e
            ) from e

    def wait_for_url_contains(
        self, url_fragment: str, timeout: int = None, error_message: str = ""
    ) -> bool:
        """Wait until the browser URL contains a specific path segment."""
        try:
            return self._get_wait(timeout).until(
                EC.url_contains(url_fragment),
                message=error_message or f"URL did not contain '{url_fragment}'",
            )
        except SeleniumTimeoutException as e:
            raise TimeoutException(
                f"Timed out waiting for URL to contain '{url_fragment}'. Current: '{self.driver.current_url}'",
                e,
            ) from e

    def wait_for_text_present(
        self, locator: tuple[By, str], text: str, timeout: int = None
    ) -> bool:
        """Wait until an element contains specific text."""
        try:
            return self._get_wait(timeout).until(
                EC.text_to_be_present_in_element(locator, text),
                message=f"Text '{text}' not found in element {locator}",
            )
        except SeleniumTimeoutException as e:
            raise TimeoutException(
                f"Timed out waiting for text '{text}' in element {locator}", e
            ) from e

    def wait_for_spinner_to_disappear(self, timeout: int = 10) -> None:
        """Wait for OrangeHRM standard async loading spinners to disappear."""
        spinner_locator = (By.CSS_SELECTOR, ".oxd-loading-spinner, .oxd-form-loader")
        try:
            # Check if any spinner is present briefly
            spinners = self.driver.find_elements(*spinner_locator)
            if spinners and spinners[0].is_displayed():
                self._get_wait(timeout).until(EC.invisibility_of_element_located(spinner_locator))
        except Exception:
            # Spinner might already be gone
            pass

    def wait_for_element_stable(self, element: WebElement, timeout: float = 3.0) -> None:
        """Verify an element position has stopped animating/moving."""
        start_time = time.time()
        last_loc = None
        while time.time() - start_time < timeout:
            try:
                curr_loc = element.location
                if last_loc is not None and curr_loc == last_loc:
                    return
                last_loc = curr_loc
                time.sleep(0.1)
            except StaleElementReferenceException:
                return
