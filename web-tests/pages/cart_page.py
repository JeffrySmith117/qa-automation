from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    _ITEMS = (By.CLASS_NAME, "cart_item")
    _CHECKOUT_BTN = (By.ID, "checkout")

    def get_item_count(self):
        return len(self.driver.find_elements(*self._ITEMS))

    def proceed_to_checkout(self):
        self.click(self._CHECKOUT_BTN)