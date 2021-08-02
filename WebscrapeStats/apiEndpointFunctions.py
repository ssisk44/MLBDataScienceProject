import requests
from datetime import date
import datetime
import calendar
import pandas as pd
from pandas.tests.extension.json import JSONArray

TeamsAbbreviations = ['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU',"KCR","LAA","LAD",'MAI','MIL','MIN','NYM','NYY','OAK','PHI','PIT',"SDP",'SFG','SEA','STL','TBD','TEX','TOR',"WSN"]
API_KEY = "86b4aafa44974957949c2312482b0f27"


def main():
    # print("https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/"+getTodaysDate()+"?"+API_KEY+"")
    getGamesbyDate()

def getTodaysDate():
    CalendarDict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                    "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    dateT = str(datetime.datetime.now().date())
    p1 = dateT[:5]
    p2 = dateT[7:]
    monthAbrev = CalendarDict[dateT[5:7]]
    return(p1 + "" + monthAbrev + "" + p2)


def getGamesbyDate():
    response = requests.get("https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/"+getTodaysDate()+"?key="+API_KEY+"")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r''+str(getTodaysDate())+'Games.csv', index=False)

def getGamesInProgress():
    response = requests.get("https://api.sportsdata.io/v3/mlb/scores/json/AreAnyGamesInProgress?key=86b4aafa44974957949c2312482b0f27")
    print(response.status_code)
    print(response.text)

def getStadiums():
    import json
    response = requests.get("https://api.sportsdata.io/v3/mlb/scores/json/Stadiums?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r'StadiumData.csv', index=False)

def activeStadiums():
    None
    #prune old stadiums from the csv

def getTeamStatsbySeason(year):
    response = requests.get("https://api.sportsdata.io/v3/mlb/scores/json/TeamSeasonStats/%7B"+str(year)+"%7D?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r""+str(year)+"TeamData.csv", index=False) #***********

def getBvP(batter,pitcher):
    "https://api.sportsdata.io/v3/mlb/stats/json/HitterVsPitcher/%7Bhitterid%7D/%7Bpitcherid%7D?key=86b4aafa44974957949c2312482b0f27"


main()