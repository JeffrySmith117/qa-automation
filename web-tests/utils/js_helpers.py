from selenium.webdriver.common.by import By


def js_click(driver, by, value):
    element = driver.find_element(by, value)
    driver.execute_script("arguments[0].click();", element)


def js_type(driver, by, value, text):
    element = driver.find_element(by, value)
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        element,
        text
    )