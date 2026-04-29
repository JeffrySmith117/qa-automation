import pytest
from utils.helpers import url

ORDER_PAYLOAD = {
    "id": 999001,
    "petId": 1,
    "quantity": 2,
    "status": "placed",
    "complete": True,
}


class TestStore:
    def test_get_inventory(self, api):
        response = api.get(url(api, "/store/inventory"))
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_create_order(self, api):
        response = api.post(url(api, "/store/order"), json=ORDER_PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ORDER_PAYLOAD["id"]
        assert data["status"] == "placed"

    def test_get_order_by_id(self, api):
        response = api.get(url(api, f"/store/order/{ORDER_PAYLOAD['id']}"))
        assert response.status_code == 200
        assert response.json()["petId"] == ORDER_PAYLOAD["petId"]

    def test_delete_order(self, api):
        response = api.delete(url(api, f"/store/order/{ORDER_PAYLOAD['id']}"))
        assert response.status_code == 200

    def test_get_deleted_order_returns_404(self, api):
        response = api.get(url(api, f"/store/order/{ORDER_PAYLOAD['id']}"))
        assert response.status_code == 404
