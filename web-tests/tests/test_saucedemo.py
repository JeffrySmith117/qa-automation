import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


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
        assert inventory.get_cart_count() >= 1
        inventory.go_to_cart()

        cart = CartPage(driver)
        assert cart.get_item_count() >= 1
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("QA", "Tester", "01310-100")
        checkout.finish_purchase()

        assert checkout.get_confirmation_message() == "Thank you for your order!"