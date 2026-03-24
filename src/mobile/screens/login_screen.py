from appium.webdriver.common.appiumby import AppiumBy

from src.mobile.screens.base_screen import BaseScreen


class LoginScreen(BaseScreen):

    USERNAME_FIELD = (AppiumBy.ACCESSIBILITY_ID, "username")
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "loginBtn")

    def enter_username(self, username: str) -> None:

        self._logger.debug(f"Entering username: {username}")
        self.enter_text(self.USERNAME_FIELD, username)

    def enter_password(self, password: str) -> None:

        self._logger.debug("Entering password (masked)")
        self.enter_text(self.PASSWORD_FIELD, password)

    def tap_login_button(self) -> None:

        self._logger.debug("Tapping login button")
        self.tap(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:

        self._logger.debug(f"Logging in as {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.tap_login_button()
