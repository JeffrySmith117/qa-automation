import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from utils.js_helpers import js_click, js_type


def test_full_purchase_e2e(driver):
    login_page = LoginPage(driver)

    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # adiciona produto ao carrinho
    js_click(driver, By.ID, "add-to-cart-sauce-labs-backpack")

    # abre carrinho
    js_click(driver, By.CLASS_NAME, "shopping_cart_link")

    # checkout
    js_click(driver, By.ID, "checkout")

    # dados do cliente
    js_type(driver, By.ID, "first-name", "QA")
    js_type(driver, By.ID, "last-name", "Tester")
    js_type(driver, By.ID, "postal-code", "12345")

    # continua checkout
    js_click(driver, By.ID, "continue")

    # finaliza compra
    js_click(driver, By.ID, "finish")

    # valida sucesso
    success_message = driver.find_element(By.CLASS_NAME, "complete-header").text

    assert success_message == "Thank you for your order!"