from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    _TITLE = (By.CLASS_NAME, "title")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def is_loaded(self):
        return self.get_text(self._TITLE) == "Products"

    def add_products(self, count=2):
        buttons = self.driver.find_elements(
            By.CSS_SELECTOR, "[data-test^='add-to-cart']"
        )
        for btn in buttons[:count]:
            btn.click()

    def get_cart_count(self):
        badges = self.driver.find_elements(*self._CART_BADGE)
        return int(badges[0].text) if badges else 0

    def go_to_cart(self):
        self.click(self._CART_ICON)