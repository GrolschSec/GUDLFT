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