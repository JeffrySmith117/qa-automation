import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


def js_click(driver, by, value):
    el = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((by, value))
    )
    driver.execute_script("arguments[0].click();", el)


class TestLogin:
    def test_successful_login(self, driver):
        LoginPage(driver).login(VALID_USER, VALID_PASS)
        assert InventoryPage(driver).is_loaded()

    def test_invalid_login_shows_error(self, driver):
        login = LoginPage(driver)
        login.login("wrong_user", "wrong_pass")
        assert "Username and password do not match" in login.get_error_message()


class TestPurchaseFlow:
    def test_add_products_to_cart(self, driver):
        LoginPage(driver).login(VALID_USER, VALID_PASS)
        inventory = InventoryPage(driver)
        inventory.add_products(count=1)
        assert inventory.get_cart_count() >= 1

    def test_full_purchase_e2e(self, driver):
        """Complete E2E: login → add product → checkout → confirm."""
        LoginPage(driver).login(VALID_USER, VALID_PASS)

        # Adiciona produto via JavaScript
        inventory = InventoryPage(driver)
        inventory.add_products(count=1)

        # Vai pro carrinho via JavaScript
        js_click(driver, By.CLASS_NAME, "shopping_cart_link")

        # Checkout via JavaScript
        js_click(driver, By.ID, "checkout")

        # Preenche dados
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        driver.find_element(By.ID, "first-name").send_keys("QA")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("01310-100")

        # Continue via JavaScript
        js_click(driver, By.ID, "continue")

        # Finish via JavaScript
        js_click(driver, By.ID, "finish")

        # Confirma mensagem
        msg = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert msg == "Thank you for your order!"