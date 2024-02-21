import pytest
from json import dumps
from database import saveClubs

def test_saveClubs(tmpdir):
    temp_file = tmpdir.join("clubs.json")
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
    ]
    saveClubs(clubs, temp_file.strpath)
    assert temp_file.read_text('utf-8') == dumps({"clubs": clubs})
