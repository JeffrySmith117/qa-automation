import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def api():
    """Shared requests session with base URL and JSON headers."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = BASE_URL
    return session
