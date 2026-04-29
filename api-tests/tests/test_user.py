import pytest
from utils.helpers import url

USER_PAYLOAD = {
    "id": 999001,
    "username": "qa_test_user",
    "firstName": "QA",
    "lastName": "Tester",
    "email": "qa@test.com",
    "password": "Test@1234",
    "phone": "11999999999",
    "userStatus": 1,
}


class TestUser:
    def test_create_user(self, api):
        response = api.post(url(api, "/user"), json=USER_PAYLOAD)
        assert response.status_code == 200

    def test_get_user_by_username(self, api):
        response = api.get(url(api, f"/user/{USER_PAYLOAD['username']}"))
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == USER_PAYLOAD["username"]
        assert data["email"] == USER_PAYLOAD["email"]

    def test_login(self, api):
        params = {"username": USER_PAYLOAD["username"], "password": USER_PAYLOAD["password"]}
        response = api.get(url(api, "/user/login"), params=params)
        assert response.status_code == 200
        assert "logged in" in response.json().get("message", "").lower()

    def test_update_user(self, api):
        updated = {**USER_PAYLOAD, "firstName": "Updated"}
        response = api.put(url(api, f"/user/{USER_PAYLOAD['username']}"), json=updated)
        assert response.status_code == 200

    def test_logout(self, api):
        response = api.get(url(api, "/user/logout"))
        assert response.status_code == 200

    def test_delete_user(self, api):
        response = api.delete(url(api, f"/user/{USER_PAYLOAD['username']}"))
        assert response.status_code == 200

    def test_get_deleted_user_returns_404(self, api):
        response = api.get(url(api, f"/user/{USER_PAYLOAD['username']}"))
        assert response.status_code == 404
