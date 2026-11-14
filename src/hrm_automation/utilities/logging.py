"""
Structured Logging Module for Enterprise HRM Automation.
Provides thread-safe, worker-aware logging with file and console outputs.
"""

import logging
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True, parents=True)

_CONFIGURED = False


def configure_logging(level: str = "INFO", worker_id: str | None = None) -> None:
    """Configure root logger with standardized formatting and worker namespace."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    worker_tag = f"[{worker_id}] " if worker_id and worker_id != "master" else ""

    log_format = (
        f"%(asctime)s [%(levelname)8s] {worker_tag}%(name)s [%(filename)s:%(lineno)d] - %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)

    # Master Execution Log
    main_log_file = LOGS_DIR / "execution.log"
    file_handler = logging.FileHandler(main_log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Worker-specific log if in parallel mode
    handlers = [console_handler, file_handler]
    if worker_id and worker_id != "master":
        worker_log_file = LOGS_DIR / f"worker_{worker_id}.log"
        worker_handler = logging.FileHandler(worker_log_file, encoding="utf-8")
        worker_handler.setLevel(logging.DEBUG)
        worker_handler.setFormatter(formatter)
        handlers.append(worker_handler)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)

    for h in handlers:
        root_logger.addHandler(h)

    # Silence noisy 3rd party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("faker").setLevel(logging.WARNING)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Retrieve a namespaced logger."""
    if not _CONFIGURED:
        worker_id = os.getenv("PYTEST_XDIST_WORKER", None)
        configure_logging(level=os.getenv("LOG_LEVEL", "INFO"), worker_id=worker_id)
    return logging.getLogger(name)
