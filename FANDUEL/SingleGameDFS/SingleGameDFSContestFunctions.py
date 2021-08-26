import datetime
import fnmatch
import math
import os
from statistics import mean
import pandas as pd
from itertools import permutations, combinations
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import scipy.stats as ss

# file = 'SingleGameContestCSVs/08182021PITLAD'  # DONT PUT .csv
# file = '08222021LAACLE'


# def main():
    ##### PREGAME

    # player_name_rank_counter()


    # playerLineupSelectorCounter(lineupSelector(150, 20, 20, 20, 20, 5, 20, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4))
    # lineupSelectortoCSVExport(lineupSelector(150, 20, 20, 20, 20, 5, 20, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4))
    # graphVsIndex()


    ##### POSTGAME
    # getFileBoxScores()
    # getBoxScoreIndex()
    # parseBStoFPPG_addFPPGtoCSV_addSCOREStoCOMBOS(getBoxScoreIndex(None), None)



    ##### MODELING AND STATISTICS
    # seabornScatterplot()
    # linearRegression('ActualDFSScore', 'PredictedDFSScore')
    # saveBoxScoresInDateRange('04012021', '08202021')


########################################################################################################################
#################################################### BEFORE GAME #######################################################
########################################################################################################################

def createCombinationsFromCSV(lineup_restriction, file, out):
    array = pd.read_csv(file + ".csv").to_numpy()
    newarray = []
    for player in range(0, len(array)): #removes injuries
        if (str(array[player][11]) == 'nan') and (int(array[player][15]) > 0):
            newarray.append(array[player])

    newarray.sort(key=lambda x: x[5], reverse=True) #sorts by predicted FPPG
    counter = 0
    while counter < len(newarray):  #adding rank to players
        newarray[counter][-1] = counter
        counter += 1

    pd.DataFrame(newarray).to_csv("ContestsOutput/" + out + str(file[21:]) + "_BEFORE_GAME_reduced_players_list.csv",
                                  index=False)

    combos = list(permutations(newarray, 5))
    permutationsarr = []
    currentlineup = []

    lineupscore = 0
    salary = 0
    playerrank = []
    playerbattingorderindex = []
    salaryMax = 35000

    for combination in range(0, len(combos)):
        for player in range(0, len(combos[combination])):
            if (salary + combos[combination][player][7]) <= salaryMax:
                currentlineup.append(combos[combination][player][3])  # add player to current
                playerrank.append(int(combos[combination][player][16]))
                playerbattingorderindex.append(combos[combination][player][15])
                salary += combos[combination][player][7]  # add salary
                if player == 0:
                    lineupscore += float(combos[combination][player][5]) * 2  # MVP
                elif player == 1:
                    lineupscore += float(combos[combination][player][5]) * 1.5  # STAR
                else:
                    lineupscore += float(combos[combination][player][5])  # NORMAL
            else:
                break

        if len(currentlineup) == 5:
            currentlineup.append(salary)
            currentlineup.append(lineupscore)

            for i in range(0, len(playerrank)):
                currentlineup.append(playerrank[i])
            currentlineup.append(mean(playerrank))

            for i in range(0, len(playerbattingorderindex)):
                currentlineup.append(playerbattingorderindex[i])
            currentlineup.append(mean(playerbattingorderindex))

            permutationsarr.append(currentlineup)

        currentlineup = []
        salary = 0
        lineupscore = 0
        playerrank = []
        playerbattingorderindex = []
    permutationsarr.sort(key=lambda x: x[6], reverse=True)

    newpermutationsarr = []  # removes the repition of every six entries being the same
    for i in range(6, len(permutationsarr) + 6):
        if i % 6 == 0 and permutationsarr[i - 6][5] >= lineup_restriction:  # every sixth and lineup cost above 30000
            newpermutationsarr.append(permutationsarr[i - 6])

    # check for all players team same and remove them
    players = pd.read_csv("ContestsOutput/" + out + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
    # print(len(newpermutationsarr))
    poplist = []
    for i in range(0, len(newpermutationsarr)):
        playerteam = []
        for j in range(0, 5):
            for k in range(0, len(players)):
                if newpermutationsarr[i][j] == players[k][3]:
                    playerteam.append(players[k][9])
                    break
        if playerteam[0] == playerteam[1] == playerteam[2] == playerteam[3] == playerteam[4]:
            poplist.append(i)
        playerteam = []

    pop_counter_deduction = 0
    for i in range(0, len(poplist)):
        newpermutationsarr.pop(poplist[i]-pop_counter_deduction) #needed to remove the proper array index after previous removal of elements
        pop_counter_deduction += 1
    # print(len(newpermutationsarr))
    # print(len(poplist))

    #save to a csv
    headers = ['Player1Name', 'Player2Name', 'Player3Name', 'Player4Name', 'Player5Name', 'Salary', 'PredictedDFSScore', "Player1Rank", "Player2Rank", "Player3Rank", "Player4Rank", "Player5Rank", "LineupMeanRank", "Player1BattingOrder", "Player2BattingOrder", "Player3BattingOrder", "Player4BattingOrder", "Player5BattingOrder", "LineupMeanBattingOrder"]
    # pd.DataFrame(newpermutationsarr).to_csv("ContestsOutput/" + out + file[21:] + "_BEFORE_GAME_lineup_permutations.csv",index=False, header=headers)
    x = pd.DataFrame(newpermutationsarr,columns=headers)
    x['Predicted DFS Score Percentile Rank'] = x.PredictedDFSScore.rank(pct=True)
    col = []
    for i in x:
        col.append(i)
    x.to_csv("ContestsOutput/" + out + file[21:] + "_BEFORE_GAME_lineup_permutations.csv",index=False, header=col)  # THIS IS FOR PERMUTATION TESTING


def player_name_rank_counter():
    permutations_array = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineup_permutations.csv").to_numpy()
    reduced_players_array = pd.read_csv(
        "ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
    player_counter_array = []
    headers = ['Player Name', "# of MVPs", "# of All Stars", "# of Regulars"]

    for name in range(0, len(reduced_players_array)):
        player_counter_array.append([reduced_players_array[name][3], 0, 0, 0])

    for i in range(0, len(permutations_array)):
        for j in range(0, len(player_counter_array)):
            for k in range(0, 5):

                if permutations_array[i][k] == player_counter_array[j][0]:
                    if k == 0:
                        player_counter_array[j][1] += 1
                    if k == 1:
                        player_counter_array[j][2] += 2
                    if k == 2 or k == 3 or k == 4:
                        player_counter_array[j][3] += 3

    pd.DataFrame(player_counter_array).to_csv(
        "ContestsOutput/" + file[21:] + "_BEFORE_GAME_player_created_lineups_distributions.csv", index=False,
        header=headers)  # THIS IS FOR PERMUTATION TESTING


def playerLineupSelectorCounter(lineupSelectorOutput):
    reduced_players_array = pd.read_csv(
        "ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
    player_counter_array = []
    headers = ['Player Name', "# of MVPs", "# of All Stars", "# of Regulars", 'Total Lineups In']

    for name in range(0, len(reduced_players_array)):
        player_counter_array.append([reduced_players_array[name][3], 0, 0, 0, 0])

    for i in range(0, len(lineupSelectorOutput)):
        for j in range(0, len(player_counter_array)):
            for k in range(0, 5):
                if lineupSelectorOutput[i][k] == player_counter_array[j][0]:
                    if k == 0:
                        player_counter_array[j][1] += 1
                    if k == 1:
                        player_counter_array[j][2] += 1
                    if k == 2 or k == 3 or k == 4:
                        player_counter_array[j][3] += 1
            player_counter_array[j][4] = player_counter_array[j][1] + player_counter_array[j][2] + player_counter_array[j][3]
    pd.DataFrame(player_counter_array).to_csv(
        "ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineup_selector_counter.csv", index=False,
        header=headers)  # THIS IS FOR PERMUTATION TESTING


def lineupSelectortoCSVExport(lineupSubmission):
    players = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
    submissionOutput = []
    for i in range(0, len(lineupSubmission)):
        submissionOutputEntry = []
        for k in range(0, 5):

            for j in range(0, len(players)):
                if lineupSubmission[i][k] == players[j][3]:
                    submissionOutputEntry.append(str(players[j][0]))
                    break

        submissionOutput.append(submissionOutputEntry)
        submissionOutputEntry = []

    headers = ['MVP - 2X Points', 'STAR - 1.5X Points', 'UTIL', 'UTIL', 'UTIL']

    pd.DataFrame(submissionOutput).to_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_contest_submition.csv",
                                          index=False, header=headers)  # THIS IS FOR PERMUTATION TESTING


########################################################################################################################
################################################## AFTER GAME ENDS #####################################################
########################################################################################################################
def getFileBoxScore(date):
    response = requests.get('https://api.sportsdata.io/v3/mlb/stats/json/BoxScores/' + str(
        getDateFormatted(date)) + '?key=86b4aafa44974957949c2312482b0f27')
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r"C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores/" + date[0:8] + "_all_box_scores.csv", index=False)

def getBoxScoreIndex(file):
    array = pd.read_csv("C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores/" + file[22:30] + "_all_box_scores.csv").to_numpy()
    team_abbreviations = ['MIL', 'PIT', 'CIN', 'PHI', 'ATL', 'WSH', 'BAL', 'BOS', 'CLE', 'DET', 'CHC', 'MIA', 'NYY',
                          'CHW', 'STL', 'KC', 'TB', 'MIN', 'OAK', 'TEX', 'COL', 'SF', 'HOU', 'LAA', 'SD', 'ARI', 'TOR',
                          'SEA', 'LAD', 'NYM']
    index = 0
    for i in range(0, len(array)):
        res = eval(array[i][0])
        date = str(list(res.values())[5][5:7] + list(res.values())[5][8:10] + list(res.values())[5][0:4])
        awayteam = list(res.values())[6]
        hometeam = list(res.values())[7]
        # print(date, awayteam, hometeam)
        # print(file[22:30], file[30:33], file[33:36])
        # print('\n')

        if date == file[22:30] and awayteam == file[30:32] and hometeam == file[32:35] and file[
                                                                                           31:33] in team_abbreviations and file[
                                                                                                                            33:35] in team_abbreviations:  ############# BOTH 2 LETTER ABBREVIATIONS
            return i

        elif date == file[22:30] and awayteam == file[30:32] and hometeam == file[32:35] and file[
                                                                                             30:32] in team_abbreviations and file[
                                                                                                                              32:35] in team_abbreviations:  ############# 2 THEN 3 LETTER ABBREVIATION
            return i
        elif date == file[22:30] and awayteam == file[30:33] and hometeam == file[33:35] and file[
                                                                                             30:33] in team_abbreviations and file[
                                                                                                                              33:35] in team_abbreviations:  ############# 3 THEN 2 LETTER ABBREVIATION
            return i

        elif date == file[22:30] and awayteam == file[30:33] and hometeam == file[33:36] and file[
                                                                                             30:33] in team_abbreviations and file[
                                                                                                                              33:36] in team_abbreviations:  ############# BOTH 3 LETTER ABBREVIATIONS
            return i

def parseBStoFPPG_addFPPGtoCSV_addSCOREStoCOMBOS(index, file, out):
    players = pd.read_csv("C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores/" + file[22:30] + "_all_box_scores.csv").to_numpy()
    # print("Box Score MLB Game Index = " + str(index))
    newarr = eval(players[index][3])
    playerstats = pd.DataFrame(newarr)
    columnslist = playerstats.columns

    # pd.DataFrame(newarr).to_csv(r"ContestsOutput/" + file[22:] + "_AFTER_GAME_player_stats.csv", index=False)
    # newarr = pd.read_csv("ContestsOutput/" + file[22:] + "_AFTER_GAME_player_stats.csv").to_numpy()
    # SCORING FOR ONE GAME DFS: MVP, ALL-STAR, 3 NORMAL
    ### 1B = 3    2B = 6    3B = 9    HR = 12   BB = 3   HBP = 3   R = 3.2   RBI = 3.5   SB = 6
    ### 42         43       44         45       50        51        40         46         55

    playersandscores = []
    headers = ['Name', 'Singles', 'Doubles', 'Triples', 'Home Runs', 'Walks', 'HBP', 'R', 'RBI', 'SB', 'Points']
    newarr = pd.DataFrame(newarr, columns=columnslist).to_numpy()

    #gets scrambled float to get player stats
    scrambledfloat = 9999999999.99
    for i in range(0, len(newarr)):
        arr = [newarr[i][39], newarr[i][40], newarr[i][41], scrambledfloat]
        scrambledfloat = min(i for i in arr if i > 0)


    for i in range(0, len(newarr)):
        name = str(newarr[i][5])
        for letter in range(0,len(name)):  ### Adding player to new list without injuries and starting..... THIS IS THE SPECIAL CHARACTER FILTER FOR PLAYER NAMES
            if name[letter] == 'í':
                name = str(name[0:letter] + 'i' + name[letter + 1:])
            elif newarr[i][5][letter] == 'ú':
                name = str(name[0:letter] + 'u' + name[letter + 1:])
            elif newarr[i][5][letter] == 'á':
                name = str(name[0:letter] + 'a' + name[letter + 1:])
            elif newarr[i][5][letter] == 'ñ':
                name = str(name[0:letter] + 'n' + name[letter + 1:])
            elif newarr[i][5][letter] == 'é':
                name = str(name[0:letter] + 'e' + name[letter + 1:])

        score = round(newarr[i][42] / scrambledfloat) * 3 + round(newarr[i][43] / scrambledfloat) * 6 + round(
            newarr[i][44] / scrambledfloat) * 9 + round(newarr[i][45] / scrambledfloat) * 12 + round(
            newarr[i][50] / scrambledfloat) * 3 + round(newarr[i][51] / scrambledfloat) * 3 + round(
            newarr[i][40] / scrambledfloat) * 3.2 + round(newarr[i][46] / scrambledfloat) * 3.5 + round(
            newarr[i][55] / scrambledfloat) * 6
        playersandscores.append(
            [name, round(newarr[i][42] / scrambledfloat), round(newarr[i][43] / scrambledfloat),
             round(newarr[i][44] / scrambledfloat), round(newarr[i][45] / scrambledfloat),
             round(newarr[i][50] / scrambledfloat), round(newarr[i][51] / scrambledfloat),
             round(newarr[i][40] / scrambledfloat), round(newarr[i][46] / scrambledfloat),
             round(newarr[i][55] / scrambledfloat), score])


    # playersandscores.sort(key=lambda x: x[-1], reverse=True)
    playersandscores = pd.DataFrame(playersandscores, columns=headers).to_numpy()
    # pd.DataFrame(playersandscores).to_csv(r"ContestsOutput/" + file[22:] + "_AFTER_GAME_player_dfs_scores.csv",
    #                                       index=False, header=headers)

    players = pd.read_csv("ContestsOutput/" + out + file[22:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
    # playersandscores = pd.read_csv("ContestsOutput/" + file[22:] + "_AFTER_GAME_player_dfs_scores.csv").to_numpy()
    players = pd.DataFrame(players)
    players['DFS_Score'] = ""
    players['DFS_Score_Rank'] = ""
    players = players.to_numpy()
    scores = []
    for i in range(0, len(players)):
        for j in range(0, len(playersandscores)):
            if players[i][3] == playersandscores[j][0]:
                players[i][-2] = playersandscores[j][-1]
                scores.append(playersandscores[j][-1])
    score_rank = ss.rankdata(scores)
    for i in range(0, len(score_rank)):
        players[i][-1] = int(math.ceil(len(score_rank) - score_rank[i] + 1)) ###depends on number of entries

    pd.DataFrame(players).to_csv("ContestsOutput/" + out + file[22:] + "_AFTER_GAME_reduced_player_list_with_scores.csv",index=False)

    # for i in range(0,len(newarr)):  ### Adding player to new list without injuries and starting..... THIS IS THE SPECIAL CHARACTER FILTER FOR PLAYER NAMES
    #     name = str(newarr[i][3])
    #     for letter in range(0, len(name)):
    #         if newarr[i][3][letter] == 'í':
    #             name = str(name[0:letter] + 'i' + name[letter + 1:])
    #         elif newarr[i][3][letter] == 'ú':
    #             name = str(name[0:letter] + 'u' + name[letter + 1:])
    #         elif newarr[i][3][letter] == 'á':
    #             name = str(name[0:letter] + 'a' + name[letter + 1:])
    #         elif newarr[i][3][letter] == 'ñ':
    #             name = str(name[0:letter] + 'n' + name[letter + 1:])
    #         elif newarr[i][3][letter] == 'é':
    #             name = str(name[0:letter] + 'e' + name[letter + 1:])

    columns_list = []
    permutations = pd.read_csv("ContestsOutput/" + out + file[22:] + "_BEFORE_GAME_lineup_permutations.csv", dtype=object)
    permutations['ActualDFSScore'] = ''
    for col in permutations:
        columns_list.append(col)
    permutations = permutations.to_numpy()
    # playerandscores = pd.read_csv("ContestsOutput/" + file[22:] + "_AFTER_GAME_reduced_player_list_with_scores.csv", dtype=object).to_numpy()

    for i in range(0,len(permutations)):
        totalscore = 0
        for j in range(0, len(playersandscores)):
            for k in range(0,5):
                if playersandscores[j][0] == permutations[i][k]:
                    if k==0:
                        totalscore += float(playersandscores[j][-1]) * 2
                    elif k==1:
                        totalscore += float(playersandscores[j][-1]) * 1.5
                    else:
                        totalscore += float(playersandscores[j][-1])

        permutations[i][-1] = totalscore
    permutations = pd.DataFrame(permutations, columns=columns_list)
    permutations['Predicted DFS Score Percentile Rank'] = permutations.PredictedDFSScore.rank(pct=True)
    permutations['Actual DFS Score Percentile Rank'] = permutations.ActualDFSScore.rank(pct=True)
    permutations['Player1PostGameRank'] = 0
    permutations['Player2PostGameRank'] = 0
    permutations['Player3PostGameRank'] = 0
    permutations['Player4PostGameRank'] = 0
    permutations['Player5PostGameRank'] = 0
    columns_list = []
    for col in permutations:
        columns_list.append(col)
    permutations = permutations.to_numpy()
    for i in range(0, len(permutations)):
        permutations[i][22] = (players[int(permutations[i][7])][18])
        permutations[i][23] = (players[int(permutations[i][8])][18])
        permutations[i][24] = (players[int(permutations[i][9])][18])
        permutations[i][25] = (players[int(permutations[i][10])][18])
        permutations[i][26] = (players[int(permutations[i][11])][18])




    permutations = sorted(permutations, key=lambda x: x[21], reverse=True)
    pd.DataFrame(permutations).to_csv("ContestsOutput/" + out + file[22:] + "_AFTER_GAME_permutations_with_scores.csv",
                           index=False, header=columns_list)
    # x = pd.read_csv("ContestsOutput/" + out + file[22:] + "_AFTER_GAME_permutations_with_scores.csv", dtype=object)
    # print(x.head(5))

########################################################################################################################
########################################   VISUALIZATION AND STATISTICS  ###############################################
########################################################################################################################
def seabornScatterplot():
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'SalaryTotal', 'PredictedDFSScore', 'ActualDFSScore',
               'Predicted DFS Score Percentile Rank', 'Actual DFS Score Percentile Rank']
    array = pd.read_csv("ContestsOutput/" + file[22:] + "_AFTER_GAME_permutations_with_scores_and_percentiles.csv")
    array = array[array['SalaryTotal'] >= 00000]
    # array = array[array['Actual DFS Score Percentile Rank'] >= .750000000000000000]
    print(len(array))

    # sns.scatterplot(array['Actual DFS Score Percentile Rank'], array['ActualDFSScore'], array['SalaryTotal'],alpha=.1).set(title="Predicted DFS Percentile vs. Actual DFS Score Outcome")
    # plt.show()

    sns.scatterplot(array['SalaryTotal'], array['Predicted DFS Score Percentile Rank'], array['ActualDFSScore'],
                    alpha=1).set(title="Predicted DFS Percentile vs. Actual DFS Score Outcome")
    plt.show()


def linearRegression(x_name, y_name):
    # headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'SalaryTotal', 'PredictedDFSScore', 'ActualDFSScore','Predicted DFS Score Percentile Rank', 'Actual DFS Score Percentile Rank']
    array = pd.read_csv("ContestsOutput/" + file[22:] + "_AFTER_GAME_permutations_with_scores_and_percentiles.csv")

    headers = []
    for col in array.columns:
        headers.append(col)

    arrayN = array.to_numpy()
    x = arrayN[:, headers.index(x_name)].reshape(-1, 1)
    y = arrayN[:, headers.index(y_name)].reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)

    print("Title: \t", x_name, 'vs.', y_name, "Linear Regression")
    print('Intercept: \t', model.intercept_)
    print('Slope: \t', model.coef_)
    print('Coefficient of Determination(R^2): \t', r_sq)

    sns.regplot(x=x_name, y=y_name, data=array).set(title=(x_name + ' vs. ' + y_name))
    plt.show()


########################################################################################################################
############################################## Additional Functions ####################################################
########################################################################################################################
def getTodaysDate():
    CalendarDict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                    "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    dateT = str(datetime.datetime.now().date())
    p1 = dateT[:5]
    p2 = dateT[7:]
    monthAbrev = CalendarDict[dateT[5:7]]
    return p1 + "" + monthAbrev + "" + p2

def getDateFormatted(date):  # entered 01012021
    CalendarDict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                    "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    day = date[2:4]
    year = date[4:8]
    monthAbrev = CalendarDict[str(date[0:2])]
    x = str(year + '-' + monthAbrev + '-' + day)
    return x

def getPlayerIndex(name):
    players = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
    for i in range(0,len(players)):
        if players[i][3] == name:
            return i

def saveBoxScoresInDateRange(date_begin, date_end):  # saveBoxScoresInDateRange('08092021', '08172021')
    daterange_begin_datetime = getDateFormattedtoDatetime(date_begin)
    daterange_end_datetime = getDateFormattedtoDatetime(date_end)
    duration = daterange_end_datetime - daterange_begin_datetime

    current_date = None
    for i in range(0, int(duration.days)):
        if i == 0:
            current_date = daterange_begin_datetime
        if checkBoxScoresDirectory(current_date) == True:
            print("Existing box score FOUND from date:", str(current_date)[0:10])
        else:
            print("NO box score found for date:", str(current_date)[0:10])
            date_for_API = getDateFormatedforAPI(str(current_date)[0:10])
            response = requests.get(
                'https://api.sportsdata.io/v3/mlb/stats/json/BoxScores/' + date_for_API + '?key=86b4aafa44974957949c2312482b0f27')
            data = response.json()
            dfItem = pd.DataFrame.from_records(data)
            dfItem.to_csv(r"C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores/" + str(
                str(current_date)[5:7] + str(current_date)[8:10] + str(current_date)[0:4]) + "_all_box_scores.csv",
                          index=False)
        current_date = current_date + datetime.timedelta(days=1)

def checkBoxScoresDirectory(current_date):
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores'
    current_date = str(str(current_date)[5:7] + str(current_date)[8:10] + str(current_date)[0:4])
    for filename in os.listdir(directory):
        # print(filename)
        # print(current_date+"_all_box_scores.csv")
        if fnmatch.fnmatch(filename, current_date+"_all_box_scores.csv"):
            return True

    return False

def getDateFormatedforAPI(date):  # entered 01012021
    CalendarDict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                    "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    day = date[8:]
    year = date[0:4]
    monthAbrev = CalendarDict[date[5:7]]
    date_for_API = str(year + '-' + monthAbrev + '-' + day)
    return date_for_API

def getDateFormattedtoDatetime(date):  # date entered like 01012021
    day = 0
    month = 0

    if date[0] == '0':
        day = int(date[1])
    else:
        day = int(date[0:2])

    if date[2] == '0':
        month = int(date[3])
    else:
        month = int(date[2:4])

    year = int(date[4:8])
    return datetime.datetime(year, day, month)


# main()
createCombinationsFromCSV(0, 'SingleGameContestCSVs/08252021LADSD', '/ALL')
# parseBStoFPPG_addFPPGtoCSV_addSCOREStoCOMBOS(getBoxScoreIndex('SingleGameContestCSVs/08222021LAACLE'), 'SingleGameContestCSVs/08222021LAACLE', "ALL/")

