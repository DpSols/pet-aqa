import allure

from src.web.pages.login_page import LoginPage
from src.web.pages.inventory_page import InventoryPage
from src.web.pages.cart_page import CartPage, CheckoutPage


class WebSteps:

    def __init__(
        self,
        login_page: LoginPage,
        inventory_page: InventoryPage,
        cart_page: CartPage,
    ) -> None:

        self._login_page = login_page
        self._inventory_page = inventory_page
        self._cart_page = cart_page

    @allure.step("Login as: {username}")
    def login_as(self, username: str, password: str) -> None:

        self._login_page.login(username, password)

    @allure.step("Add items to cart: {items}")
    def add_items_to_cart(self, items: list[str]) -> None:

        for item in items:
            self._inventory_page.add_item_to_cart(item)

    @allure.step("Complete checkout: {first_name} {last_name}")
    def complete_checkout(self, first_name: str, last_name: str, zip_code: str) -> str:

        self._inventory_page.open_cart()
        self._cart_page.proceed_to_checkout()
        checkout_page = CheckoutPage(self._cart_page.page)
        checkout_page.fill_information(first_name, last_name, zip_code)
        confirmation = checkout_page.finish()
        return confirmation
