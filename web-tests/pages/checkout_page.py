from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _ZIP_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")
    _FINISH_BTN = (By.ID, "finish")
    _CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_customer_info(self, first, last, zip_code):
        self.type(self._FIRST_NAME, first)
        self.type(self._LAST_NAME, last)
        self.type(self._ZIP_CODE, zip_code)
        self.click(self._CONTINUE_BTN)

    def finish_purchase(self):
        self.click(self._FINISH_BTN)

    def get_confirmation_message(self):
        return self.get_text(self._CONFIRMATION_HEADER)
