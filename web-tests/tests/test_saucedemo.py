from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    ).send_keys("QA")

    driver.find_element(By.ID, "last-name").send_keys("Tester")
    driver.find_element(By.ID, "postal-code").send_keys("12345")

    continue_button = wait.until(
        EC.presence_of_element_located((By.ID, "continue"))
    )

    driver.execute_script("arguments[0].click();", continue_button)

    finish_button = wait.until(
        EC.presence_of_element_located((By.ID, "finish"))
    )

    driver.execute_script("arguments[0].click();", finish_button)

    success_message = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    ).text

    assert success_message == "Thank you for your order!"