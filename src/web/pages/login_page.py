"""Sauce Demo login page object."""

from src.web.pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page for Sauce Demo."""

    # Locators
    USERNAME_INPUT = "input[data-test='username']"
    PASSWORD_INPUT = "input[data-test='password']"
    LOGIN_BUTTON = "input[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def login(self, username: str, password: str) -> None:
        """Log in to Sauce Demo.

        Args:
            username: Username.
            password: Password.
        """

        self._logger.debug(f"Logging in as {username}")
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self._logger.debug("Login button clicked")

    def get_error_message(self) -> str:
        """Get error message if login failed.

        Returns:
            Error message text.
        """

        return self.get_text(self.ERROR_MESSAGE)
