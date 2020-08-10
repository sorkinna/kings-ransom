import pandas as pd
import statsapi
import requests
import json
from datetime import datetime

def within_date(dateString):
    year = int(dateString.split("-")[0])
    if year > 2007 and year < 2020:
        return True
    else:
        return False

class Player:
    name = ""
    hand = ""
    playerFile = None

    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.playerFile = open(
            "players/" + name.replace(" ", "_").replace(".", "") + ".txt", "a")


def read_pitches():
    f = open("log.txt", "a")
    for x in range(490000, 500000):
        f.write(str(x) + "\n")
        pitchCountHome = 0
        pitchCountAway = 0
        url = "http://statsapi.mlb.com/api/v1.1/game/%s/feed/live" % x
        response = requests.get(url)
        if(response.status_code == 200) and (response.json()["gameData"]["game"]["type"] == "R") and (response.json()["gameData"]["teams"]["away"]["sport"]["id"] == 1):
            homePitcher = None
            awayPitcher = None
            hasOut = False
            outs = 0
            date = response.json()["gameData"]["datetime"]["originalDate"]
            if within_date(date):
                print(x)
                print(date)
                print(response.json()["gameData"]["teams"]["away"]["name"] + " at " + response.json()["gameData"]["teams"]["home"]["name"])
                f.write(date + "\n")
                f.write(response.json()["gameData"]["teams"]["away"]["name"] + " at " + response.json()["gameData"]["teams"]["home"]["name"] + "\n")
                for atBat in response.json()["liveData"]["plays"]["allPlays"]:
                    if hasOut and "event" in result.keys():
                        if ("Double Play" in result["event"]) or ("DP" in result["event"]):
                            outs = outs + 2
                        elif result["event"] is 'Triple Play':
                            outs = outs + 3
                        else:
                            outs = outs + 1
                    outs = outs % 3
                    batter = atBat["matchup"]["batter"]["fullName"]
                    pitcher = atBat["matchup"]["pitcher"]["fullName"]
                    batHand = atBat["matchup"]["batSide"]["code"]
                    pitchHand = atBat["matchup"]["pitchHand"]["code"]
                    strikes = 0
                    balls = 0
                    isTopInning = atBat["about"]["isTopInning"]
                    hasOut = atBat["about"]["hasOut"]
                    result = atBat["result"]
                    if (homePitcher is None) and (isTopInning == True):
                        homePitcher = Player(pitcher, pitchHand)
                    if (awayPitcher is None) and (isTopInning == False):
                        awayPitcher = Player(pitcher, pitchHand)
                    for pitch in atBat["playEvents"]:
                        if pitch["isPitch"]:
                            data = pitch["pitchData"]
                            if "type" in pitch["details"].keys():
                                pitchType = pitch["details"]["type"]["description"]
                            else:
                                pitchType = "N/A"
                            if "event" in result.keys():
                                playEvent = result["event"]
                            else:
                                playEvent = "N/A"
                            printString = pitcher + "|" + pitchHand + "|" + batter + "|" + batHand + "|" + \
                                playEvent + "|" + pitch["details"]["call"]["code"] + "|" + pitchType +\
                                "|" + "%d" + "|" + "%d" + "|" + "%d" + "|" + "%d" + "|" + "%d" + "|" + "%d"
                            if "zone" in data.keys() and "startSpeed" in data.keys():
                                zone = data["zone"]
                                startSpeed = data["startSpeed"]
                            else:
                                zone = 0
                                startSpeed = 0
                            if isTopInning:
                                finalPrint = (printString % (pitchCountHome, balls, strikes, outs, zone, startSpeed))
                                homePitcher.playerFile.write(finalPrint + "\n")
                                pitchCountHome = pitchCountHome + 1
                            else:
                                finalPrint = (printString % (pitchCountAway, balls, strikes, outs, zone, startSpeed))
                                awayPitcher.playerFile.write(finalPrint + "\n")
                                pitchCountAway = pitchCountAway + 1
                            if pitch["details"]["call"]["code"] == "*B" or pitch["details"]["call"]["code"] == "B":
                                balls = balls + 1
                            else:
                                if strikes < 2:
                                    strikes = strikes + 1
                        else:
                            if "eventType" in pitch["details"]:
                                if pitch["details"]["eventType"] == "pitching_substitution":
                                    pitcherChangeRequest = requests.get(
                                        "http://statsapi.mlb.com" + pitch["player"]["link"])
                                    if(pitcherChangeRequest.status_code == 200):
                                        pitchName = pitcherChangeRequest.json()[
                                            "people"][0]["fullName"]
                                        newPitchHand = pitcherChangeRequest.json(
                                        )["people"][0]["pitchHand"]["code"]
                                        if isTopInning:
                                            homePitcher = Player(
                                                pitchName, newPitchHand)
                                            pitchCountHome = 0
                                        else:
                                            awayPitcher = Player(
                                                pitchName, newPitchHand)
                                            pitchCountAway = 0


if __name__ == '__main__':
    startTime = datetime.now()
    read_pitches()
    print(datetime.now() - startTime)
