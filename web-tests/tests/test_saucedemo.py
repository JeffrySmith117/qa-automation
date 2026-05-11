from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from utils.js_helpers import js_click, js_type


def test_full_purchase_e2e(driver):
    login_page = LoginPage(driver)

    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    js_click(driver, By.ID, "add-to-cart-sauce-labs-backpack")
    js_click(driver, By.CLASS_NAME, "shopping_cart_link")
    js_click(driver, By.ID, "checkout")

    js_type(driver, By.ID, "first-name", "QA")
    js_type(driver, By.ID, "last-name", "Tester")
    js_type(driver, By.ID, "postal-code", "12345")

    js_click(driver, By.ID, "continue")

    finish_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    )

    finish_button.click()

    success_message = driver.find_element(By.CLASS_NAME, "complete-header").text

    assert success_message == "Thank you for your order!"