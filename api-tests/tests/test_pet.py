import pytest
from utils.helpers import url

PET_PAYLOAD = {
    "id": 999001,
    "name": "Rex",
    "status": "available",
    "photoUrls": ["https://example.com/rex.jpg"],
}


class TestPet:
    def test_create_pet(self, api):
        response = api.post(url(api, "/pet"), json=PET_PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == PET_PAYLOAD["id"]
        assert data["name"] == PET_PAYLOAD["name"]

    def test_get_pet_by_id(self, api):
        response = api.get(url(api, f"/pet/{PET_PAYLOAD['id']}"))
        assert response.status_code == 200
        assert response.json()["name"] == PET_PAYLOAD["name"]

    def test_update_pet(self, api):
        updated = {**PET_PAYLOAD, "status": "sold"}
        response = api.put(url(api, "/pet"), json=updated)
        assert response.status_code == 200
        assert response.json()["status"] == "sold"

    def test_find_pets_by_status(self, api):
        response = api.get(url(api, "/pet/findByStatus"), params={"status": "available"})
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert all(p["status"] == "available" for p in pets if "status" in p)

    def test_delete_pet(self, api):
        response = api.delete(url(api, f"/pet/{PET_PAYLOAD['id']}"))
        assert response.status_code == 200

    def test_get_deleted_pet_returns_404(self, api):
        response = api.get(url(api, f"/pet/{PET_PAYLOAD['id']}"))
        assert response.status_code == 404
