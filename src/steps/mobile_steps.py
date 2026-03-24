import allure

from src.mobile.screens.login_screen import LoginScreen
from src.mobile.screens.home_screen import HomeScreen


class MobileSteps:

    def __init__(self, login_screen: LoginScreen, home_screen: HomeScreen) -> None:

        self._login_screen = login_screen
        self._home_screen = home_screen

    @allure.step("Login on mobile: {username}")
    def login(self, username: str, password: str) -> None:

        self._login_screen.login(username, password)

    @allure.step("Verify home screen is visible")
    def verify_home_visible(self) -> bool:

        return self._home_screen.is_visible()
