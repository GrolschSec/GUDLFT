import json
from flask import Flask, render_template, request, redirect, flash, url_for
from database import CLUBS, COMPETITIONS


app = Flask(__name__)
app.secret_key = "something_special"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in CLUBS if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=COMPETITIONS)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in CLUBS if c["name"] == club][0]
    foundCompetition = [c for c in COMPETITIONS if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=COMPETITIONS)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in COMPETITIONS if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in CLUBS if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    if placesRequired > int(club["points"]):
        flash("You don't have enough points to complete booking!")
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=COMPETITIONS)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
