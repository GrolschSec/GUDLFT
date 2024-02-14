from json import load, dump


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = load(comps)["competitions"]
        return listOfCompetitions


def saveClubs(clubs, filename="clubs.json"):
    with open(filename, "w") as c:
        dump({"clubs": clubs}, c)


def saveCompetitions(competitions, filename="competitions.json"):
    with open(filename, "w") as comps:
        dump({"competitions": competitions}, comps)


CLUBS = loadClubs()

COMPETITIONS = loadCompetitions()


def saveToDB(app):
    if not app.config["TESTING"]:
        saveClubs(CLUBS)
        saveCompetitions(COMPETITIONS)
