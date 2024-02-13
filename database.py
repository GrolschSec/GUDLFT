from json import load, dump


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = load(comps)["competitions"]
        return listOfCompetitions


def saveClubs(clubs):
    with open("clubs.json", "w") as c:
        dump({"clubs": clubs}, c)


def saveCompetitions(competitions):
    with open("competitions.json", "w") as comps:
        dump({"competitions": competitions}, comps)


CLUBS = loadClubs()

COMPETITIONS = loadCompetitions()
