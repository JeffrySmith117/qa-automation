from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    _ITEMS = (By.CLASS_NAME, "cart_item")
    _CHECKOUT_BTN = (By.ID, "checkout")

    def get_item_count(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_contents"))
        )
        return len(self.driver.find_elements(*self._ITEMS))

    def proceed_to_checkout(self):
        self.click(self._CHECKOUT_BTN)