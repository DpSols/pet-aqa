import pytest

from config.settings import Settings
from src.mobile.driver_factory import create_driver
from src.mobile.screens.login_screen import LoginScreen
from src.mobile.screens.home_screen import HomeScreen
from src.steps.mobile_steps import MobileSteps


@pytest.fixture(scope="function")
def appium_driver(settings: Settings):
    driver = create_driver(settings.mobile)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_screen(appium_driver) -> LoginScreen:
    return LoginScreen(appium_driver)


@pytest.fixture(scope="function")
def home_screen(appium_driver) -> HomeScreen:
    return HomeScreen(appium_driver)


@pytest.fixture(scope="function")
def mobile_steps(
    login_screen: LoginScreen,
    home_screen: HomeScreen,
) -> MobileSteps:
    return MobileSteps(login_screen, home_screen)
