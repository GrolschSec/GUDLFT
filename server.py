from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
from database import CLUBS, COMPETITIONS, saveToDB


def is_past_competition(competition):
    return datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now()


app = Flask(__name__)
app.secret_key = "something_special"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    if request.form["email"] not in [club["email"] for club in CLUBS]:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for("index"))
    club = [club for club in CLUBS if club["email"] == request.form["email"]][0]
    for competition in COMPETITIONS:
        competition.setdefault("is_past", is_past_competition(competition))
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
    if club.get(competition["name"]) is None:
        club[competition["name"]] = 0
    if is_past_competition(competition):
        flash("You can't book places for past competitions!")
    elif placesRequired > int(club["points"]):
        flash("You don't have enough points to complete booking!")
    elif placesRequired > 12 or club[competition["name"]] + placesRequired > 12:
        flash("You can't buy more than 12 places per competition!")
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        club[competition["name"]] += placesRequired
        club["points"] = str(int(club["points"]) - placesRequired)
        saveToDB(app)
        flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=COMPETITIONS)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
