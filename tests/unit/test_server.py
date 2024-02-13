import pytest
from server import app

class TestClubsPointsDisplay:
	def test_clubs_points_display_all_clubs(self, client, clubs):
		response = client.get('/clubs')
		assert response.status_code == 200
		for club in clubs:
			assert club['name'] in response.get_data(as_text=True)
