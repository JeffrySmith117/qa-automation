from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    _TITLE = (By.CLASS_NAME, "title")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def is_loaded(self):
        return self.get_text(self._TITLE) == "Products"

    def add_products(self, count=1):
        added = 0
        while added < count:
            buttons = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[contains(@data-test,'add-to-cart')]")
                )
            )
            buttons[0].click()
            added += 1

    def get_cart_count(self):
        badges = self.driver.find_elements(*self._CART_BADGE)
        return int(badges[0].text) if badges else 0

    def go_to_cart(self):
        self.click(self._CART_ICON)