import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    """Chrome reinicia a cada teste para evitar problemas de estado."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()