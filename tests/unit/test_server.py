import pytest


class TestShowSummary:
    def test_show_summary_with_valid_email(self, client, clubs):
        valid_email = next(club["email"] for club in clubs)
        response = client.post("/showSummary", data={"email": valid_email})
        assert response.status_code == 200

    def test_show_summary_with_invalid_email(self, client):
        invalid_email = "invalid@test.com"
        response = client.post(
            "/showSummary", data={"email": invalid_email}, follow_redirects=True
        )
        assert response.status_code == 200
        assert "Sorry, that email wasn&#39;t found." in response.get_data(as_text=True)
