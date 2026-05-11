import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


def js_click(driver, by, value):
    el = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((by, value))
    )
    driver.execute_script("arguments[0].click();", el)


def js_type(driver, by, value, text):
    el = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((by, value))
    )
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
        el, text
    )


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

        inventory = InventoryPage(driver)
        inventory.add_products(count=1)

        js_click(driver, By.CLASS_NAME, "shopping_cart_link")
        js_click(driver, By.ID, "checkout")

        # Preenche dados via JavaScript
        js_type(driver, By.ID, "first-name", "first-name", "QA")
        js_type(driver, By.ID, "last-name", "last-name", "Tester")
        js_type(driver, By.ID, "postal-code", "postal-code", "01310100")

        js_click(driver, By.ID, "continue")

        # Espera pagina de overview
        WebDriverWait(driver, 15).until(
            EC.url_contains("checkout-step-two")
        )

        js_click(driver, By.ID, "finish")

        msg = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert msg == "Thank you for your order!"