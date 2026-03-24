import allure
import pytest

from src.steps.web_steps import WebSteps


@allure.feature("Sauce Demo Web")
@allure.story("Checkout Flow")
@pytest.mark.web
class TestCheckoutFlow:

    @allure.title("Standard user can complete checkout")
    def test_standard_user_can_checkout(self, web_steps: WebSteps) -> None:
        web_steps.login_as("standard_user", "secret_sauce")

        web_steps.add_items_to_cart(["Sauce Labs Backpack", "Sauce Labs Bike Light"])

        confirmation = web_steps.complete_checkout("John", "Doe", "12345")

        assert "THANK YOU FOR YOUR ORDER" in confirmation, \
            f"Expected 'THANK YOU FOR YOUR ORDER' in '{confirmation}'"
