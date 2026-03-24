import pytest
from loguru import logger

from config.logging_config import configure_logging


def pytest_sessionstart(session: pytest.Session) -> None:
    configure_logging()
    logger.info("Test session started")


def pytest_runtest_setup(item: pytest.Item) -> None:
    logger.info(f"Running test: {item.nodeid}")


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    if report.when == "call":
        duration = report.duration or 0
        if report.outcome == "passed":
            logger.info(f"Test PASSED in {duration:.2f}s")
        elif report.outcome == "failed":
            logger.error(f"Test FAILED in {duration:.2f}s")
        elif report.outcome == "skipped":
            logger.warning(f"Test SKIPPED in {duration:.2f}s")
