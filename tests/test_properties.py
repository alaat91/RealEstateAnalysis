from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_and_list_property() -> None:
    payload = {
        "title": "Test apartment in Eriksberg",
        "city": "Göteborg",
        "area": "Eriksberg",
        "address": "Testgatan 1",
        "ownership_type": "bostadsratt",
        "property_type": "apartment",
        "asking_price_sek": 3_750_000,
        "monthly_fee_sek": 5_200,
        "living_area_sqm": 72,
        "rooms": 3,
        "latitude": 57.7069,
        "longitude": 11.9389,
        "source_url": "https://example.com/property/1",
        "description": "A test property used by CI.",
    }

    create_response = client.post("/api/v1/properties", json=payload)
    assert create_response.status_code == 201, create_response.text
    created = create_response.json()
    assert created["id"]
    assert created["city"] == "Göteborg"

    list_response = client.get("/api/v1/properties?city=Göteborg")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1
