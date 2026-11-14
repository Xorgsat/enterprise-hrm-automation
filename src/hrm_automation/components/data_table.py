"""
Data Table Component.
Encapsulates OrangeHRM tabular data grids (.oxd-table).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.core.base_page import BasePage
from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)


class DataTableComponent(BasePage):
    """Encapsulates interactions with OrangeHRM dynamic table grids."""

    TABLE_CONTAINER = (By.CSS_SELECTOR, ".oxd-table")
    HEADER_CELLS = (By.CSS_SELECTOR, ".oxd-table-header .oxd-table-th")
    BODY_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-card")
    CELLS = (By.CSS_SELECTOR, ".oxd-table-cell")
    NO_RECORDS_MESSAGE = (
        By.CSS_SELECTOR,
        ".oxd-text--span:contains('No Records Found'), .orangehrm-horizontal-padding",
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_table_displayed(self, timeout: int = 10) -> bool:
        """Verify the table grid is rendered."""
        return self.is_visible(self.TABLE_CONTAINER, timeout=timeout)

    def get_column_headers(self) -> list[str]:
        """Retrieve cleaned list of column header titles."""
        headers = self.find_all(self.HEADER_CELLS)
        return [h.text.replace("\n", " ").strip() for h in headers if h.text.strip()]

    def get_row_count(self) -> int:
        """Return the number of visible rows in the table body."""
        return len(self.find_all(self.BODY_ROWS))

    def get_cell_text(self, row_index: int, col_index: int) -> str:
        """Retrieve text from a specific row and column (1-indexed)."""
        locator = (
            By.XPATH,
            f"//div[contains(@class,'oxd-table-body')]/div[contains(@class,'oxd-table-card')][{row_index}]"
            f"/div[contains(@class,'oxd-table-row')]/div[contains(@class,'oxd-table-cell')][{col_index}]",
        )
        return self.get_text(locator)

    def find_row_index_by_text(self, target_text: str, timeout: int = 6) -> int | None:
        """Find the 1-indexed row number containing the target text anywhere in its cells."""
        self.wait_for_page_readiness()
        xpath = (
            f"//div[contains(@class,'oxd-table-body')]//div[contains(@class,'oxd-table-card')]"
            f"[contains(., '{target_text}')]"
        )
        try:
            self.wait.wait_for_presence((By.XPATH, xpath), timeout=timeout)
            return 1
        except Exception:
            try:
                table_body = self.driver.find_element(By.CSS_SELECTOR, ".oxd-table-body")
                if target_text in table_body.text:
                    return 1
            except Exception:
                pass
            return None

    def click_action_for_record(self, record_text: str, action_icon_title: str = "edit") -> None:
        """
        Click an action icon (edit, trash/delete, approve) on the row containing record_text.
        """
        row_idx = self.find_row_index_by_text(record_text)
        if not row_idx:
            raise ValueError(f"Record with text '{record_text}' not found in table.")

        # OrangeHRM action buttons usually contain specific SVG or bi-pencil/bi-trash classes
        action_locator = (
            By.XPATH,
            f"//div[contains(@class,'oxd-table-body')]/div[contains(@class,'oxd-table-card')][{row_idx}]"
            f"//button[contains(@class,'oxd-icon-button')][.//i[contains(@class,'{action_icon_title}')]]",
        )
        self.click(action_locator)
