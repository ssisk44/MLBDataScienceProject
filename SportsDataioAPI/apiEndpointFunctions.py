import requests
import datetime
import pandas as pd
import numpy as np

API_KEY = "86b4aafa44974957949c2312482b0f27"


def main():
    None #Sike

#########################
##### MLB GAME DATA #####
#########################

### GAME DATA ###
def getTodaysDate():
    CalendarDict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                    "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    dateT = str(datetime.datetime.now().date())
    p1 = dateT[:5]
    p2 = dateT[7:]
    monthAbrev = CalendarDict[dateT[5:7]]
    return p1 + "" + monthAbrev + "" + p2

def getGamesByDate():
    response = requests.get(
        "https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/" + getTodaysDate() + "?key=" + API_KEY + "")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r'outCSV/' + str(getTodaysDate()) + 'Games.csv', index=False)

def getGamesInProgress():
    response = requests.get(
        "https://api.sportsdata.io/v3/mlb/scores/json/AreAnyGamesInProgress?key=86b4aafa44974957949c2312482b0f27")
    print(response.status_code)
    print(response.text)



### STADIUM DATA ###
def getStadiums():  # ONE TIME ONLY
    response = requests.get(
        "https://api.sportsdata.io/v3/mlb/scores/json/Stadiums?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r'outCSV/StadiumData.csv', index=False)
    # remove old stadiums

def getActiveStadiums(): #ONE TIME ONLY
    allStadiums = pd.read_csv("outCSV/StadiumData.csv")
    column_names = allStadiums.columns.tolist()

    # allStadiums = allStadiums.to_numpy()
    # newarray = []
    # i = 0
    # while i < len(allStadiums):
    #     if (str(allStadiums[i][5]) == 'USA') or (str(allStadiums[i][5]) == 'Canada'):
    #         print(i, allStadiums[i][5])
    #         newarray.append(allStadiums[i])
    #         i += 1
    #     else:
    #         i += 1
    # pd.DataFrame(newarray).to_csv(r'outCSV/ActiveStadiumData.csv', index=False, header=column_names)



### PLAYER DATA ###
def getBvP(batter, pitcher):
    "https://api.sportsdata.io/v3/mlb/stats/json/HitterVsPitcher/%7Bhitterid%7D/%7Bpitcherid%7D?key=86b4aafa44974957949c2312482b0f27"



### TEAM DATA ###
def getTeams():  # ONE TIME ONLY
    response = requests.get("https://api.sportsdata.io/v3/mlb/scores/json/teams?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r'outCSV/MLBTeams.csv', index=False)

def getTeamPlayers(team):
    response = requests.get(
        "https://api.sportsdata.io/v3/mlb/scores/json/Players/" + team + "?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r'outCSV/' + str(getTodaysDate()) + str(team) + 'StadiumData.csv', index=False)

def getTeamStatsBySeason(year):
    response = requests.get("https://api.sportsdata.io/v3/mlb/scores/json/TeamSeasonStats/%7B" + str(
        year) + "%7D?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r"outCSV/" + str(year) + "TeamData.csv", index=False)  # ***********










main()
