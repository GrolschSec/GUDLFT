import pytest


class TestPurchasePlaces:
    def test_purchase_places_less_than_12_places(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Winter Showdown",
                "club": "Simply Lift",
                "places": "6",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" in response.get_data(as_text=True)

    def test_purchase_places_more_than_12_places(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Winter Showdown",
                "club": "Simply Lift",
                "places": "13",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" not in response.get_data(as_text=True)
        assert (
            "You can&#39;t buy more than 12 places per competition!"
            in response.get_data(as_text=True)
        )

    def test_purchase_places_more_than_12_in_2_times(self, client):
        data = {
                "competition": "Winter Showdown",
                "club": "Simply Lift",
                "places": "7",
        }
        client.post(
            "/purchasePlaces",
            data=data,
        )
        response = client.post(
            "/purchasePlaces",
            data=data,
        )
        assert response.status_code == 200
        assert "Great-booking complete!" not in response.get_data(as_text=True)
        assert (
            "You can&#39;t buy more than 12 places per competition!"
            in response.get_data(as_text=True)
        )
