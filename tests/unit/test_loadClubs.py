import pytest
from database import loadClubs


def test_loadClubs(mock_file, monkeypatch):
	monkeypatch.setattr("builtins.open", mock_file)
	clubs = loadClubs()
	assert clubs[2]['name'] == 'She Lifts'