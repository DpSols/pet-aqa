import allure
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger


class BaseScreen:

    def __init__(self, driver: WebDriver) -> None:

        self.driver = driver
        self._logger = logger.bind(layer="mobile", screen=self.__class__.__name__)

    def find_element(self, locator: tuple):

        return self.driver.find_element(*locator)

    def tap(self, locator: tuple) -> None:

        self._logger.debug(f"Tapping element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("mobile: tap", {"element": element.id})

    def enter_text(self, locator: tuple, text: str) -> None:

        self._logger.debug(f"Entering text into {locator}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:

        text = self.find_element(locator).text
        self._logger.debug(f"Got text: {text}")
        return text

    def wait_for_visible(self, locator: tuple, timeout: int = 10) -> None:

        self._logger.debug(f"Waiting for visibility: {locator}")
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def take_screenshot(self, name: str) -> None:

        self._logger.debug(f"Taking screenshot: {name}")
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name, allure.attachment_type.PNG)
