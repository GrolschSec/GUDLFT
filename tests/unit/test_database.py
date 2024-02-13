import pytest
from database import loadClubs, loadCompetitions, saveClubs, saveCompetitions
from json import dumps

def test_loadClubs(mock_file, monkeypatch):
	monkeypatch.setattr("builtins.open", mock_file)
	clubs = loadClubs()
	assert clubs[2]['name'] == 'She Lifts'

def test_loadCompetitions(mock_file, monkeypatch):
	monkeypatch.setattr("builtins.open", mock_file)
	clubs = loadCompetitions()
	assert clubs[0]['name'] == 'Spring Festival'
