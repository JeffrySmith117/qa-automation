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

    def add_products(self, count=2):
        for i in range(count):
            btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
                )
            )
            btn.click()
            # Espera o botão mudar para "Remove" confirmando que foi adicionado
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-test^='remove']")
                )
            )

    def get_cart_count(self):
        badges = self.driver.find_elements(*self._CART_BADGE)
        return int(badges[0].text) if badges else 0

    def go_to_cart(self):
        self.click(self._CART_ICON)