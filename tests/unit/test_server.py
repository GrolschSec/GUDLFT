import pytest
from datetime import datetime
from bs4 import BeautifulSoup


class TestShowSummary:
    @pytest.fixture
    def setup(self, client):
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        soup = BeautifulSoup(response.get_data(as_text=True), "html.parser")
        competitions = soup.find_all("li")
        return competitions

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
                    "You can't book places for past competitions"
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
                assert "Booking complete!" in response.get_data(as_text=True)
                assert (
                    "You can't book places for past competitions"
                    not in response.get_data(as_text=True)
                )
