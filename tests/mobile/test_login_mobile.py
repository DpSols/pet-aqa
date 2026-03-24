import allure
import pytest

from src.steps.mobile_steps import MobileSteps


@allure.feature("Mobile App")
@allure.story("Authentication")
@pytest.mark.mobile
class TestMobileLogin:

    @allure.title("Valid user can log in on mobile")
    def test_valid_login(self, mobile_steps: MobileSteps) -> None:
        mobile_steps.login("username", "password")

        assert mobile_steps.verify_home_visible(), \
            "Home screen should be visible after successful login"
