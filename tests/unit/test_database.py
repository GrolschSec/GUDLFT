import pytest
from database import loadClubs, loadCompetitions, saveClubs, saveCompetitions
from json import load, dumps

def test_loadClubs(mock_file, monkeypatch):
	monkeypatch.setattr("builtins.open", mock_file)
	clubs = loadClubs()
	assert clubs[2]['name'] == 'She Lifts'

def test_loadCompetitions(mock_file, monkeypatch):
	monkeypatch.setattr("builtins.open", mock_file)
	clubs = loadCompetitions()
	assert clubs[0]['name'] == 'Spring Festival'

def test_saveClubs(tmpdir):
    temp_file = tmpdir.join("clubs.json")
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
    ]
    saveClubs(clubs, temp_file.strpath)
    assert temp_file.read_text('utf-8') == dumps({"clubs": clubs})

def test_saveCompetitions(tmpdir):
	temp_file = tmpdir.join("competitions.json")
	competitions = [
		{"name": "Spring Festival", "date": "2018-04-01", "competitors": "Simply Lift, She Lifts"},
		{"name": "Fall Classic", "date": "2018-09-15", "competitors": "Iron Temple, She Lifts"}
	]
	saveCompetitions(competitions, temp_file.strpath)
	assert temp_file.read_text('utf-8') == dumps({"competitions": competitions})

