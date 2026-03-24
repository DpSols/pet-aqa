import allure
from playwright.sync_api import Page
from loguru import logger


class BasePage:

    def __init__(self, page: Page) -> None:

        self.page = page
        self._logger = logger.bind(layer="web", page=self.__class__.__name__)

    def navigate(self, url: str) -> None:

        self._logger.debug(f"Navigating to {url}")
        self.page.goto(url)

    def click(self, locator: str) -> None:

        self._logger.debug(f"Clicking: {locator}")
        self.page.locator(locator).click()

    def fill(self, locator: str, value: str) -> None:

        self._logger.debug(f"Filling {locator} with value (masked)")
        self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:

        text = self.page.locator(locator).text_content()
        self._logger.debug(f"Got text from {locator}: {text}")
        return text or ""

    def wait_for_element(self, locator: str, timeout: int = 30000) -> None:

        self._logger.debug(f"Waiting for element: {locator}")
        self.page.locator(locator).wait_for(timeout=timeout)

    def take_screenshot(self, name: str) -> None:

        self._logger.debug(f"Taking screenshot: {name}")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name, allure.attachment_type.PNG)
