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
        wait = WebDriverWait(driver, 30)

        LoginPage(driver).login(VALID_USER, VALID_PASS)

        # Adiciona produto pelo ID fixo — mais estável no CI
        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "add-to-cart-sauce-labs-backpack")
            )
        ).click()

        # Vai pro carrinho
        js_click(driver, By.CLASS_NAME, "shopping_cart_link")

        # Checkout
        wait.until(EC.url_contains("cart"))
        js_click(driver, By.ID, "checkout")

        # Preenche formulário
        wait.until(EC.url_contains("checkout-step-one"))
        wait.until(
            EC.visibility_of_element_located((By.ID, "first-name"))
        ).send_keys("QA")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("12345")

        js_click(driver, By.ID, "continue")

        # Finaliza
        wait.until(EC.url_contains("checkout-step-two"))
        finish = wait.until(
            EC.presence_of_element_located((By.ID, "finish"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", finish)
        driver.execute_script("arguments[0].click();", finish)

        # Confirma
        wait.until(EC.url_contains("checkout-complete"))
        msg = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert msg == "Thank you for your order!"