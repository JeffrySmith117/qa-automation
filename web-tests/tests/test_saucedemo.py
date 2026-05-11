from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_full_purchase_e2e(driver):
    wait = WebDriverWait(driver, 30)

    # abre site
    driver.get("https://www.saucedemo.com/")

    # login
    wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(
        By.ID,
        "password"
    ).send_keys("secret_sauce")

    driver.find_element(
        By.ID,
        "login-button"
    ).click()

    # espera inventário carregar
    wait.until(
        EC.url_contains("inventory")
    )

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

    # espera checkout step one
    wait.until(
        EC.url_contains("checkout-step-one")
    )

    # formulário
    wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    ).send_keys("QA")

    driver.find_element(
        By.ID,
        "last-name"
    ).send_keys("Tester")

    driver.find_element(
        By.ID,
        "postal-code"
    ).send_keys("12345")

    # continue
    wait.until(
        EC.element_to_be_clickable((By.ID, "continue"))
    ).click()

    # espera checkout step two
    wait.until(
        EC.url_contains("checkout-step-two")
    )

    # finish
    finish_button = wait.until(
        EC.element_to_be_clickable((By.ID, "finish"))
    )

    driver.execute_script(
        "arguments[0].scrollIntoView(true);",
        finish_button
    )

    driver.execute_script(
        "arguments[0].click();",
        finish_button
    )

    # espera página final
    wait.until(
        EC.url_contains("checkout-complete")
    )

    # valida sucesso
    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    )

    assert success_message.text == "Thank you for your order!"