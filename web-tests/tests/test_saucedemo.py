from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fill_input(driver, element_id, value):
    element = driver.find_element(By.ID, element_id)

    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, element, value)


def test_full_purchase_e2e(driver):
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.saucedemo.com/")

    wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")

    driver.find_element(By.ID, "login-button").click()

    wait.until(
        EC.element_to_be_clickable(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        )
    ).click()

    wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    ).click()

    wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )

    fill_input(driver, "first-name", "QA")
    fill_input(driver, "last-name", "Tester")
    fill_input(driver, "postal-code", "12345")

    continue_button = driver.find_element(By.ID, "continue")

    driver.execute_script(
        "arguments[0].click();",
        continue_button
    )

    wait.until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )

    finish_button = driver.find_element(By.ID, "finish")

    driver.execute_script(
        "arguments[0].click();",
        finish_button
    )

    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    ).text

    assert success_message == "Thank you for your order!"