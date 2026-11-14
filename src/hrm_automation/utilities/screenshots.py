"""
Diagnostic Screenshot Capture Utility.
Captures viewports on test failures and registers them with Allure and local disk.
"""

from datetime import datetime
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from hrm_automation.utilities.logging import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
SCREENSHOTS_DIR = BASE_DIR / "artifacts" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def capture_screenshot(
    driver: WebDriver,
    name: str = "failure",
    directory: Path | None = None,
    attach_to_allure: bool = True,
) -> Path | None:
    """Capture a screenshot, save to disk, and attach to Allure if available."""
    if not driver:
        return None

    target_dir = directory or SCREENSHOTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)
    file_path = target_dir / f"{safe_name}_{timestamp}.png"

    try:
        success = driver.save_screenshot(str(file_path))
        if success:
            logger.info(f"Diagnostic screenshot captured: {file_path}")

            if attach_to_allure:
                try:
                    import allure
                    from allure_commons.types import AttachmentType

                    with open(file_path, "rb") as image_file:
                        allure.attach(
                            image_file.read(),
                            name=f"Screenshot_{safe_name}",
                            attachment_type=AttachmentType.PNG,
                        )
                except ImportError:
                    pass
            return file_path
        else:
            logger.warning(f"Failed to capture screenshot for '{name}'")
            return None
    except Exception as e:
        logger.error(f"Exception during screenshot capture: {e}")
        return None
