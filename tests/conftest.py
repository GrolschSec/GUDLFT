import pytest
from server import app


@pytest.fixture
def competitions():
    data = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
    ]
    return data


@pytest.fixture
def clubs():
    data = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    return data


@pytest.fixture
def client(monkeypatch, competitions, clubs):
    app.config["TESTING"] = True
    monkeypatch.setattr("server.competitions", competitions)
    monkeypatch.setattr("server.clubs", clubs)
    with app.test_client() as client:
        yield client
