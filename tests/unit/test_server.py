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


class TestPurchasePlaces:
    def test_purchase_places_valid_amount(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Spring Festival",
                "places": "4",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" in response.get_data(as_text=True)

    def test_purchase_places_invalid_amount(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Iron Temple",
                "competition": "Spring Festival",
                "places": "100",
            },
        )
        assert response.status_code == 200
        assert "Great-booking complete!" not in response.get_data(as_text=True)
        assert (
            "You don&#39;t have enough points to complete booking!"
            in response.get_data(as_text=True)
        )
