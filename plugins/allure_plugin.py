import pytest
import allure

from config.settings import Settings
from config.allure_config import AllureConfig


def pytest_configure(config: pytest.Config) -> None:
    settings = Settings()
    allure_config = AllureConfig()
    allure_config.write_all(settings)


def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    if call.when == "call" and call.excinfo is not None:
        page = item.funcargs.get("page")
        if page:
            try:
                screenshot = page.screenshot()
                allure.attach(screenshot, "failure_screenshot", allure.attachment_type.PNG)
            except Exception as e:
                print(f"Failed to attach screenshot: {e}")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        nodeid_parts = item.nodeid.split("/")
        if len(nodeid_parts) > 1:
            test_type = nodeid_parts[1]
            if test_type in ("api", "web", "mobile"):
                allure.dynamic.tag(test_type)
