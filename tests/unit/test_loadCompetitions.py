import pytest
from database import loadCompetitions


def test_loadCompetitions(mock_file, monkeypatch):
	monkeypatch.setattr("builtins.open", mock_file)
	clubs = loadCompetitions()
	assert clubs[0]['name'] == 'Spring Festival'
