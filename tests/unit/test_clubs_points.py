import pytest
from bs4 import BeautifulSoup
from datetime import datetime


class TestClubsPointsDisplay:
    def test_clubs_points_display_all_clubs(self, client, clubs):
        response = client.get("/clubs/points")
        assert response.status_code == 200
        for club in clubs:
            assert club["name"] in response.get_data(as_text=True)
