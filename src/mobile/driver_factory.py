from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from loguru import logger

from config.settings import MobileSettings


def create_driver(settings: MobileSettings):

    _logger = logger.bind(layer="mobile", component="driver_factory")
    _logger.debug(f"Creating driver for {settings.platform}")

    if settings.platform == "android":
        options = UiAutomator2Options()
        options.automation_name = "uiautomator2"
        options.platform_name = "Android"
        options.device_name = settings.device_name
        options.app = settings.app_path
        options.no_reset = False
    else:
        options = XCUITestOptions()
        options.automation_name = "XCUITest"
        options.platform_name = "iOS"
        options.device_name = settings.device_name
        options.app = settings.app_path
        options.no_reset = False

    driver = webdriver.Remote(settings.appium_url, options=options)
    _logger.info(f"Appium driver created ({settings.platform})")
    return driver
