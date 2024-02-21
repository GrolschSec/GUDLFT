import pytest
from datetime import datetime

class TestPurchasePlaces:
    def test_purchase_places_valid_amount(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Winter Showdown",
                "places": "4",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" in response.get_data(as_text=True)

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

    def test_purchase_places_invalid_amount(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Winter Showdown",
                "places": "100",
            },
        )
        assert response.status_code == 200
        assert (
            "You don&#39;t have enough points to complete booking!"
            in response.get_data(as_text=True)
        )

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

    def test_purchase_places_past_competition(self, client, competitions):
        for competition in competitions:
            response = client.post(
                "/purchasePlaces",
                data={
                    "competition": competition["name"],
                    "club": "Simply Lift",
                    "places": "1",
                },
            )
            assert response.status_code == 200
            if (
                datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
                < datetime.now()
            ):
                assert "Booking complete!" not in response.get_data(as_text=True)
                assert (
                    "You can&#39;t book places for past competitions!"
                    in response.get_data(as_text=True)
                )

    def test_purchase_places_future_competition(self, client, competitions):
        for competition in competitions:
            response = client.post(
                "/purchasePlaces",
                data={
                    "competition": competition["name"],
                    "club": "Simply Lift",
                    "places": "1",
                },
            )
            assert response.status_code == 200
            if (
                datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
                > datetime.now()
            ):
                assert "Great-booking complete!" in response.get_data(as_text=True)
                assert (
                    "You can&#39;t book places for past competitions!"
                    not in response.get_data(as_text=True)
                )

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
    
    def test_purchase_places_more_than_available(self, client, competitions):
        place_available = next((comp["numberOfPlaces"] for comp in competitions if comp["name"] == "WinShow"), None)
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "WinShow",
                "club": "Simply Lift",
                "places": f"{int(place_available) + 1}",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" not in response.get_data(as_text=True)
        assert "You can&#39;t buy more places than available!" in response.get_data(as_text=True)