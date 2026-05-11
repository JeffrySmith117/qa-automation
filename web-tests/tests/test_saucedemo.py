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

    driver.find_element(
        By.ID,
        "password"
    ).send_keys("secret_sauce")

    login_button = wait.until(
        EC.presence_of_element_located((By.ID, "login-button"))
    )

    driver.execute_script(
        "arguments[0].click();",
        login_button
    )

    # adiciona produto
    add_button = wait.until(
        EC.presence_of_element_located(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        add_button
    )

    # abre carrinho
    cart_button = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        cart_button
    )

    # checkout
    checkout_button = wait.until(
        EC.presence_of_element_located((By.ID, "checkout"))
    )

    driver.execute_script(
        "arguments[0].click();",
        checkout_button
    )

    # espera página checkout carregar
    wait.until(
        EC.url_contains("checkout-step-one")
    )

    # formulário
    first_name = wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )

    first_name.clear()
    first_name.send_keys("QA")

    last_name = driver.find_element(By.ID, "last-name")
    last_name.clear()
    last_name.send_keys("Tester")

    postal_code = driver.find_element(By.ID, "postal-code")
    postal_code.clear()
    postal_code.send_keys("12345")

    # continue
    continue_button = wait.until(
        EC.presence_of_element_located((By.ID, "continue"))
    )

    driver.execute_script(
        "arguments[0].click();",
        continue_button
    )

    # espera próxima etapa
    wait.until(
        EC.url_contains("checkout-step-two")
    )

    # finish
    finish_button = wait.until(
        EC.presence_of_element_located((By.ID, "finish"))
    )

    driver.execute_script(
        "arguments[0].click();",
        finish_button
    )

    # valida sucesso
    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    ).text

    assert success_message == "Thank you for your order!"