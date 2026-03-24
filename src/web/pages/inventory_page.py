from src.web.pages.base_page import BasePage


class InventoryPage(BasePage):

    ITEM_NAME_PATTERN = ".inventory_item_name"
    ADD_TO_CART_BUTTON_PATTERN = "button:has-text('Add to cart')"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"

    def get_item_names(self) -> list[str]:

        self._logger.debug("Getting all item names")
        items = self.page.locator(self.ITEM_NAME_PATTERN).all_text_contents()
        self._logger.debug(f"Found {len(items)} items")
        return items

    def add_item_to_cart(self, item_name: str) -> None:

        self._logger.debug(f"Adding {item_name} to cart")
        button = self.page.locator(".inventory_item").filter(has_text=item_name).locator(self.ADD_TO_CART_BUTTON_PATTERN)
        button.click()

    def open_cart(self) -> None:

        self._logger.debug("Opening cart")
        self.click(self.CART_LINK)
