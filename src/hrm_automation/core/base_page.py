"""
BasePage Object Abstraction.
Encapsulates common element interactions, stale-element recovery, explicit synchronization,
and viewport scrolling with rich diagnostic error reporting.
"""

import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from config.settings import settings
from hrm_automation.core.exceptions import (
    ElementNotFoundException,
    StaleElementRecoveryException,
    TimeoutException,
)
from hrm_automation.core.wait_manager import WaitManager
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class BasePage:
    """Foundational Page Object providing resilient interaction primitives."""

    def __init__(self, driver: WebDriver, timeout: int | None = None):
        self.driver = driver
        self.timeout = timeout or settings.default_timeout
        self.wait = WaitManager(driver, default_timeout=self.timeout)

    @property
    def current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    @property
    def title(self) -> str:
        """Return the current document title."""
        return self.driver.title

    def open_url(self, url: str) -> None:
        """Navigate directly to the specified URL and await page readiness."""
        logger.debug(f"Navigating to URL: {url}")
        try:
            self.driver.get(url)
        except Exception as e:
            logger.warning(
                f"Initial navigation to {url} hit timeout/warning ({e}); proceeding to explicit DOM wait."
            )
            try:
                self.driver.execute_script("window.stop();")
            except Exception:
                pass
        self.wait_for_page_readiness()

    def wait_for_page_readiness(self) -> None:
        """Verify document.readyState == 'complete' and OrangeHRM loaders are absent."""
        try:
            self.wait._get_wait(timeout=self.timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self.wait.wait_for_spinner_to_disappear()
        except Exception:
            pass

    def find(self, locator: tuple[By, str], timeout: int | None = None) -> WebElement:
        """Find an element after waiting for its visibility."""
        try:
            return self.wait.wait_for_visibility(locator, timeout=timeout)
        except TimeoutException as e:
            raise ElementNotFoundException(
                f"Element {locator} not found or not visible within {timeout or self.timeout}s on {self.current_url}",
                e,
            ) from e

    def find_all(self, locator: tuple[By, str], timeout: int | None = None) -> list[WebElement]:
        """Find all matching elements present in the DOM."""
        try:
            self.wait.wait_for_presence(locator, timeout=timeout)
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    def click(
        self, locator: tuple[By, str], timeout: int | None = None, max_retries: int = 3
    ) -> None:
        """Click an element with automatic stale-element recovery and scroll assistance."""
        last_exception = None
        for attempt in range(1, max_retries + 1):
            try:
                element = self.wait.wait_for_clickable(locator, timeout=timeout)
                self.scroll_into_view(element)
                element.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                last_exception = e
                logger.debug(
                    f"Click retry {attempt}/{max_retries} on {locator} due to {type(e).__name__}"
                )
                time.sleep(0.3)
            except TimeoutException as e:
                # If timeout waiting for standard clickability, try DOM query and JS click before giving up
                try:
                    elem = self.driver.find_element(*locator)
                    if elem.is_displayed():
                        logger.debug(f"Executing direct click fallback on {locator}")
                        self.driver.execute_script("arguments[0].click();", elem)
                        return
                except Exception:
                    pass
                raise ElementNotFoundException(
                    f"Cannot click {locator}: element not clickable within timeout on {self.current_url}",
                    e,
                ) from e

        # Fallback to ActionChains or JS click if intercepted by an overlay
        try:
            element = self.driver.find_element(*locator)
            ActionChains(self.driver).move_to_element(element).click().perform()
            return
        except Exception:
            try:
                element = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", element)
                return
            except Exception:
                raise StaleElementRecoveryException(
                    f"Failed to click {locator} after {max_retries} attempts.", last_exception
                ) from last_exception

    def type_text(
        self,
        locator: tuple[By, str],
        text: str,
        clear_first: bool = True,
        timeout: int | None = None,
    ) -> None:
        """Enter text into an input field, with optional clear."""
        element = self.find(locator, timeout=timeout)
        if clear_first:
            self.clear_input(element)
        element.send_keys(text)

    def clear_input(self, element: WebElement) -> None:
        """Clear an input field using both clear() and keyboard backspace sequences."""
        try:
            element.click()
        except Exception:
            pass
        try:
            element.clear()
        except Exception:
            pass
        try:
            element.send_keys(Keys.COMMAND + "a")
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACKSPACE)
            val = element.get_attribute("value") or ""
            if val:
                element.send_keys(Keys.BACKSPACE * (len(val) + 2))
        except Exception:
            pass

    def get_text(self, locator: tuple[By, str], timeout: int | None = None) -> str:
        """Retrieve visible inner text of an element."""
        element = self.find(locator, timeout=timeout)
        return element.text.strip()

    def get_attribute(
        self, locator: tuple[By, str], attribute_name: str, timeout: int | None = None
    ) -> str | None:
        """Retrieve attribute value of an element."""
        element = self.find(locator, timeout=timeout)
        return element.get_attribute(attribute_name)

    def is_visible(self, locator: tuple[By, str], timeout: int = 3) -> bool:
        """Check if an element is currently displayed without raising a fatal exception."""
        try:
            self.wait.wait_for_visibility(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_present(self, locator: tuple[By, str]) -> bool:
        """Check if an element exists in the DOM."""
        return len(self.driver.find_elements(*locator)) > 0

    def scroll_into_view(self, element: WebElement) -> None:
        """Smooth scroll element into the center of the viewport."""
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'nearest'});",
                element,
            )
        except Exception:
            pass
