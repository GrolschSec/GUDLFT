import pytest


class TestPurchasePlaces:
    def test_purchase_places_valid_amount(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Spring Festival",
                "places": "4",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" in response.get_data(as_text=True)

    def test_purchase_places_invalid_amount(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Spring Festival",
                "places": "100",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" not in response.get_data(as_text=True)
        assert (
            "You don&#39;t have enough points to complete booking!"
            in response.get_data(as_text=True)
        )
