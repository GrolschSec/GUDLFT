import pytest
from bs4 import BeautifulSoup
from datetime import datetime


class TestShowSummary:
    @pytest.fixture
    def setup(self, client):
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        soup = BeautifulSoup(response.get_data(as_text=True), "html.parser")
        competitions = soup.find_all("li")
        return competitions
    
    def test_show_summary_with_valid_email(self, client, clubs):
        valid_email = next(club["email"] for club in clubs)
        response = client.post("/showSummary", data={"email": valid_email})
        assert response.status_code == 200

    def test_show_summary_with_invalid_email(self, client):
        invalid_email = "invalid@test.com"
        response = client.post(
            "/showSummary", data={"email": invalid_email}, follow_redirects=True
        )
        assert response.status_code == 200
        assert "Sorry, that email wasn&#39;t found." in response.get_data(as_text=True)
    
    def test_show_summary_past_event_not_active(self, setup):
        for competition in setup:
            date_string = (
                competition.find("br").next_sibling.replace("Date: ", "").strip()
            )
            date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            if date < datetime.now():
                assert competition.find("a", href=True) is None

    def test_show_summary_future_event_active(self, setup):
        for competition in setup:
            date_string = (
                competition.find("br").next_sibling.replace("Date: ", "").strip()
            )
            date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            book_link = competition.find("a", href=True)
            if date > datetime.now():
                assert book_link is not None


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
