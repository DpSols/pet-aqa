from src.web.pages.base_page import BasePage


class CartPage(BasePage):

    CHECKOUT_BUTTON = "button[data-test='checkout']"

    def proceed_to_checkout(self) -> None:

        self._logger.debug("Proceeding to checkout")
        self.click(self.CHECKOUT_BUTTON)


class CheckoutPage(BasePage):

    FIRST_NAME_INPUT = "input[data-test='firstName']"
    LAST_NAME_INPUT = "input[data-test='lastName']"
    ZIP_INPUT = "input[data-test='postalCode']"
    CONTINUE_BUTTON = "input[data-test='continue']"
    FINISH_BUTTON = "button[data-test='finish']"
    CONFIRMATION_MESSAGE = ".complete-text"

    def fill_information(self, first_name: str, last_name: str, zip_code: str) -> None:

        self._logger.debug(f"Filling checkout info: {first_name} {last_name}")
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.ZIP_INPUT, zip_code)
        self.click(self.CONTINUE_BUTTON)

    def finish(self) -> str:

        self._logger.debug("Clicking finish button")
        self.click(self.FINISH_BUTTON)
        message = self.get_text(self.CONFIRMATION_MESSAGE)
        self._logger.debug(f"Checkout confirmed: {message}")
        return message
