import pytest

@pytest.fixture.usefixtures('client', 'competitions', 'clubs')
class TestPurchasePlaces:
	
	def set_up(self, monkeypatch, competitions, clubs):
		monkeypatch.setattr('server.competitions', competitions)
		monkeypatch.setattr('server.clubs', clubs)
	
	def test_purchase_places_valid_amount(self, client):
		pass
