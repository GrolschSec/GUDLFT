import pytest


class TestPurchasePlaces:
    def test_purchase_places_wallet_update(self, client, clubs):
        places = 3
        points = next(
            (club["points"] for club in clubs if club["name"] == "Simply Lift"), None
        )
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Winter Showdown",
                "club": "Simply Lift",
                "places": f"{places}",
            },
        )
        assert response.status_code == 200
        assert next(
            (club["points"] for club in clubs if club["name"] == "Simply Lift"), None
        ) == str(int(points) - places)
