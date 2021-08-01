import requests
from datetime import date
import calendar
import pandas as pd
from pandas.tests.extension.json import JSONArray

TeamsAbbreviations = ['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU',"KCR","LAA","LAD",'MAI','MIL','MIN','NYM','NYY','OAK','PHI','PIT',"SDP",'SFG','SEA','STL','TBD','TEX','TOR',"WSN"]
API_KEY = "86b4aafa44974957949c2312482b0f27"

def getDate(date):
    today = date
    Month = calendar.month_name[today.month]
    MonthAbbrev = str(Month[0:3].upper())
    Year = today.year
    Day = today.day
    date = (str(Year) + "-" + str(MonthAbbrev) + "-" + str(Day))
    return date

def getGamesbyDate():

    print(("https://api.sportsdata.io/v3/mlb/scores/xml/GamesByDate/{"+getDate(date.today())+"}?"+API_KEY))
    # response = requests.get("https://api.sportsdata.io/v3/mlb/scores/xml/GamesByDate/{"+getDate(date.today())+"}?"+key+"")
    # print(response.status_code)
    # print(response)

# string = str("https://api.sportsdata.io/v3/mlb/scores/json/Stadiums?"+API_KEY)
# response = requests.get("https://api.sportsdata.io/v3/mlb/scores/json/Stadiums?"+API_KEY)
# print(response.status_code)
# print(response)
#
# print(string)
# print(response.status_code)


# https://api.sportsdata.io/v3/mlb/scores/json/Stadiums?key=86b4aafa44974957949c2312482b0f27
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