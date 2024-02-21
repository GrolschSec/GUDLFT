import pytest
from json import dumps
from database import saveCompetitions

def test_saveCompetitions(tmpdir):
	temp_file = tmpdir.join("competitions.json")
	competitions = [
		{"name": "Spring Festival", "date": "2018-04-01", "competitors": "Simply Lift, She Lifts"},
		{"name": "Fall Classic", "date": "2018-09-15", "competitors": "Iron Temple, She Lifts"}
	]
	saveCompetitions(competitions, temp_file.strpath)
	assert temp_file.read_text('utf-8') == dumps({"competitions": competitions})

