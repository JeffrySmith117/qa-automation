import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


def js_click(driver, by, value):
    el = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((by, value))
    )
    driver.execute_script("arguments[0].click();", el)


def fill_field(driver, field_id, text):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    driver.execute_script(
        f"document.getElementById('{field_id}').value = '{text}';"
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
        wait = WebDriverWait(driver, 30)

        LoginPage(driver).login(VALID_USER, VALID_PASS)

        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "add-to-cart-sauce-labs-backpack")
            )
        ).click()

        js_click(driver, By.CLASS_NAME, "shopping_cart_link")
        wait.until(EC.url_contains("cart"))

        js_click(driver, By.ID, "checkout")
        wait.until(EC.url_contains("checkout-step-one"))

        fill_field(driver, "first-name", "QA")
        fill_field(driver, "last-name", "Tester")
        fill_field(driver, "postal-code", "12345")

        # Debug
        print("first-name:", driver.find_element(By.ID, "first-name").get_attribute("value"))
        print("last-name:", driver.find_element(By.ID, "last-name").get_attribute("value"))
        print("postal-code:", driver.find_element(By.ID, "postal-code").get_attribute("value"))

        js_click(driver, By.ID, "continue")

        wait.until(EC.url_contains("checkout-step-two"))

        finish = wait.until(
            EC.element_to_be_clickable((By.ID, "finish"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", finish)
        driver.execute_script("arguments[0].click();", finish)

        wait.until(EC.url_contains("checkout-complete"))
        msg = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert msg == "Thank you for your order!"