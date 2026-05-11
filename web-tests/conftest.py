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
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(20)
    driver.set_page_load_timeout(30)

    yield driver
    driver.quit()