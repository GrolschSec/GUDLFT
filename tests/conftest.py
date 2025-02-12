import pytest
from server import app
from io import StringIO
from json import dumps


@pytest.fixture
def competitions():
    data = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
        {
            "name": "Winter Showdown",
            "date": "2024-12-05 11:00:00",
            "numberOfPlaces": "14",
        },
        {
            "name": "WinShow",
            "date": "2024-12-05 11:00:00",
            "numberOfPlaces": "4",
        },
    ]
    return data


@pytest.fixture
def clubs():
    data = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "14"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    return data


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def common_setup(monkeypatch, competitions, clubs):
    monkeypatch.setattr("server.COMPETITIONS", competitions)
    monkeypatch.setattr("server.CLUBS", clubs)

@pytest.fixture
def mock_file():
    def _mock_file(file, mode='r'):
        clubs_data = dumps({
            "clubs": [
                {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
                {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
                {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
            ]
        })
        competitions_data = dumps({
            "competitions": [
                {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
                {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"}
            ]
        })
        if 'clubs.json' in file:
            return StringIO(clubs_data)
        elif 'competitions.json' in file:
            return StringIO(competitions_data)
    return _mock_file