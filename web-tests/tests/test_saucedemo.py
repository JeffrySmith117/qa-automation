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
        inventory.add_products(count=2)
        assert inventory.get_cart_count() == 2

    def test_full_purchase_e2e(self, driver):
        """Complete E2E: login → add products → checkout → confirm."""
        # Login direto — scope=function garante browser limpo
        LoginPage(driver).login(VALID_USER, VALID_PASS)

        # Adiciona 2 produtos
        inventory = InventoryPage(driver)
        inventory.add_products(count=2)

        # Verifica badge antes de ir ao carrinho
        assert inventory.get_cart_count() == 2

        inventory.go_to_cart()

        # Verifica itens no carrinho
        cart = CartPage(driver)
        assert cart.get_item_count() == 2
        cart.proceed_to_checkout()

        # Finaliza compra
        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("QA", "Tester", "01310-100")
        checkout.finish_purchase()

        assert checkout.get_confirmation_message() == "Thank you for your order!"