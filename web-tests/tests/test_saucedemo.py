from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_full_purchase_e2e(driver):
    wait = WebDriverWait(driver, 20)

    # abre site
    driver.get("https://www.saucedemo.com/")

    # login
    wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")

    wait.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    ).click()

    # adiciona produto
    wait.until(
        EC.element_to_be_clickable(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        )
    ).click()

    # abre carrinho
    wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    ).click()

    # checkout
    wait.until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    ).click()

    # espera formulário aparecer
    wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    ).send_keys("QA")

    driver.find_element(By.ID, "last-name").send_keys("Tester")
    driver.find_element(By.ID, "postal-code").send_keys("12345")

    # continua
    wait.until(
        EC.element_to_be_clickable((By.ID, "continue"))
    ).click()

    # finish
    wait.until(
        EC.element_to_be_clickable((By.ID, "finish"))
    ).click()

    # valida mensagem
    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    ).text

    assert success_message == "Thank you for your order!"