import pytest
from datetime import datetime

class TestShowSummary:
    def test_show_summary_past_event_not_active(self, client):
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        html = response.get_data(as_text=True)
        

class TestPurchasePlaces:
	def test_purchase_places_past_competition(self, client):
		pass