from appium.webdriver.common.appiumby import AppiumBy

from src.mobile.screens.base_screen import BaseScreen


class HomeScreen(BaseScreen):

    TITLE = (AppiumBy.ACCESSIBILITY_ID, "appHeaderText")

    def get_title(self) -> str:

        return self.get_text(self.TITLE)

    def is_visible(self) -> bool:

        try:
            self.wait_for_visible(self.TITLE, timeout=5)
            self._logger.debug("Home screen is visible")
            return True
        except Exception as e:
            self._logger.warning(f"Home screen not visible: {e}")
            return False
