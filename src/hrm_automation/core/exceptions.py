"""
Custom Framework Exceptions with Contextual Diagnostics.
Preserves original underlying exceptions and diagnostic state.
"""


class HRMAutomationException(Exception):
    """Base exception for all HRM automation framework errors."""

    def __init__(self, message: str, original_exception: Exception | None = None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

    def __str__(self) -> str:
        if self.original_exception:
            return f"{self.message} | Caused by: {type(self.original_exception).__name__}: {self.original_exception}"
        return self.message


class TimeoutException(HRMAutomationException):
    """Raised when an explicit wait synchronization condition exceeds duration."""

    pass


class ElementNotFoundException(HRMAutomationException):
    """Raised when a specified element locator cannot be located on the page."""

    pass


class StaleElementRecoveryException(HRMAutomationException):
    """Raised when an element remains stale after multiple retry recovery attempts."""

    pass


class WorkflowExecutionException(HRMAutomationException):
    """Raised when an end-to-end business workflow fails to complete expected transitions."""

    pass


class ConfigurationException(HRMAutomationException):
    """Raised when invalid framework configuration or environment settings are provided."""

    pass


class EnvironmentUnreachableException(HRMAutomationException):
    """Raised when target application environment is unreachable or down."""

    pass
