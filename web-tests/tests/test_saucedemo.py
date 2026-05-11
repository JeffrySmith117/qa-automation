from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from utils.js_helpers import js_click


def test_full_purchase_e2e(driver):
    login_page = LoginPage(driver)

    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # adiciona produto
    js_click(driver, By.ID, "add-to-cart-sauce-labs-backpack")

    # abre carrinho
    js_click(driver, By.CLASS_NAME, "shopping_cart_link")

    # checkout
    js_click(driver, By.ID, "checkout")

    # preenche formulário
    driver.find_element(By.ID, "first-name").send_keys("QA")
    driver.find_element(By.ID, "last-name").send_keys("Tester")
    driver.find_element(By.ID, "postal-code").send_keys("12345")

    # continua
    js_click(driver, By.ID, "continue")

    # espera botão finish aparecer
    finish_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    )

    finish_button.click()

    # valida compra
    success_message = driver.find_element(By.CLASS_NAME, "complete-header").text

    assert success_message == "Thank you for your order!"