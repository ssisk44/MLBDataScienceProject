import datetime
import fnmatch
import os

import pandas as pd
from itertools import permutations, combinations
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import ast

file = 'SingleGameContestCSVs/08182021PITLAD'  # DONT PUT .csv


def main():
    ##### PREGAME
    # createCombinationsFromCSV()
    # player_name_rank_counter()
    # playerLineupSelectorCounter(lineupSelector(150, 20, 20, 20, 20, 5, 20, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4))
    # lineupSelectortoCSVExport(lineupSelector(150, 20, 20, 20, 20, 5, 20, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4))
    # graphVsIndex()


    ##### POSTGAME
    # getAllBoxScores()
    # getBoxScoreIndex()
    # parseBoxScoretoPointsPerPlayer(getBoxScoreIndex())
    # addPlayerScoretoCSV()
    # editCombinationsWITHPlayerScores()
    saveBoxScoresInDateRange('04012021', '08192021')

    ##### MODELING AND STATISTICS
    # seabornScatterplot()
    # linearRegression('ActualDFSScore', 'PredictedDFSScore')


########################################################################################################################
#################################################### BEFORE GAME #######################################################
########################################################################################################################

def createCombinationsFromCSV():
    array = pd.read_csv(file + ".csv").to_numpy()
    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11]) == 'nan') and (int(array[player][15]) > 0):
            newarray.append(array[player])
    newarray.sort(key=lambda x: x[5], reverse=True)
    pd.DataFrame(newarray).to_csv("ContestsOutput/" + str(file[21:]) + "_BEFORE_GAME_reduced_players_list.csv",
                                  index=False)
    combos = list(permutations(newarray, 5))
    permutationsarr = []
    currentlineup = []
    lineupscore = 0
    salary = 0
    salaryMax = 35000

    for combination in range(0, len(combos)):
        for player in range(0, len(combos[combination])):
            if (salary + combos[combination][player][7]) <= salaryMax:
                currentlineup.append(combos[combination][player][3])  # add player to current
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
            permutationsarr.append(currentlineup)
        currentlineup = []
        salary = 0
        lineupscore = 0
    permutationsarr.sort(key=lambda x: x[6], reverse=True)

    newpermutationsarr = []  # removes the repition of every six entries being the same
    for i in range(6, len(permutationsarr) + 6):
        if i % 6 == 0 and permutationsarr[i - 6][5] >= 32000:  # every sixth and lineup cost above 30000
            newpermutationsarr.append(permutationsarr[i - 6])

    # check for all players team same and remove them
    players = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
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
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Salary', 'LineupScore']
    pd.DataFrame(newpermutationsarr).to_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineup_permutations.csv",index=False, header=headers)  # THIS IS FOR PERMUTATION TESTING


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


def lineupSelector(numEntries, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16):
    numEntries = 150
    lineups = []
    permutations = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineup_permutations.csv").to_numpy()
    players = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()

    # First Player
    lineup_counter = 0
    while lineup_counter <= P1:
        for i in range(0, len(permutations)):
            if lineup_counter >= P1:
                break
            elif permutations[i][0] == players[0][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 2nd Player
    lineup_counter = 0
    while lineup_counter <= P2:
        for i in range(0, len(permutations)):
            if lineup_counter >= P2:
                break
            elif permutations[i][0] == players[1][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 3rd Player
    lineup_counter = 0
    while lineup_counter <= P3:
        for i in range(0, len(permutations)):
            if lineup_counter >= P3:
                break
            elif permutations[i][0] == players[2][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 4th Player
    lineup_counter = 0
    while lineup_counter <= P4:
        for i in range(0, len(permutations)):
            if lineup_counter >= P4:
                break
            elif permutations[i][0] == players[3][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 5th Player
    lineup_counter = 0
    while lineup_counter <= P5:
        for i in range(0, len(permutations)):
            if lineup_counter >= P5:
                break
            elif permutations[i][0] == players[4][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 6th Player
    lineup_counter = 0
    while lineup_counter <= P6:
        for i in range(0, len(permutations)):
            if lineup_counter >= P6:
                break
            elif permutations[i][0] == players[5][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 7th Player
    lineup_counter = 0
    while lineup_counter <= P7:
        for i in range(0, len(permutations)):
            if lineup_counter >= P7:
                break
            elif permutations[i][0] == players[6][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 8th Player
    lineup_counter = 0
    while lineup_counter <= P8:
        for i in range(0, len(permutations)):
            if lineup_counter >= P8:
                break
            elif permutations[i][0] == players[7][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 9th Player
    lineup_counter = 0
    while lineup_counter <= P9:
        for i in range(0, len(permutations)):
            if lineup_counter >= P9:
                break
            elif permutations[i][0] == players[8][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 10th Player
    lineup_counter = 0
    while lineup_counter <= P10:
        for i in range(0, len(permutations)):
            if lineup_counter >= P10:
                break
            elif permutations[i][0] == players[9][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 11th Player
    lineup_counter = 0
    while lineup_counter <= P11:
        for i in range(0, len(permutations)):
            if lineup_counter >= P11:
                break
            elif permutations[i][0] == players[10][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 12th Player
    lineup_counter = 0
    while lineup_counter <= P12:
        for i in range(0, len(permutations)):
            if lineup_counter >= P12:
                break
            elif permutations[i][0] == players[11][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 13th Player
    lineup_counter = 0
    while lineup_counter <= P13:
        for i in range(0, len(permutations)):
            if lineup_counter >= P13:
                break
            elif permutations[i][0] == players[12][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 14th Player
    lineup_counter = 0
    while lineup_counter <= P14:
        for i in range(0, len(permutations)):
            if lineup_counter >= P14:
                break
            elif permutations[i][0] == players[13][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 15th Player
    lineup_counter = 0
    while lineup_counter <= P15:
        for i in range(0, len(permutations)):
            if lineup_counter >= P15:
                break
            elif permutations[i][0] == players[14][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # 16th Player
    lineup_counter = 0
    while lineup_counter <= P16:
        for i in range(0, len(permutations)):
            if lineup_counter >= P16:
                break
            elif permutations[i][0] == players[15][3]:
                lineups.append(permutations[i])
                lineup_counter += 1
        break

    # for i in range(0, len(lineups)):
    #     print(str(lineups[i][5]), str(lineups[i][6]))
    # print("Number of lineups created: " + str(len(lineups)))

    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Salary', 'LineupScore']
    pd.DataFrame(lineups).to_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineups_selected.csv", index=False,
                                 header=headers)

    return lineups


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
def getAllBoxScores():
    response = requests.get('https://api.sportsdata.io/v3/mlb/stats/json/BoxScores/' + str(
        getDateFormatted()) + '?key=86b4aafa44974957949c2312482b0f27')
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r"DailyBoxScores/" + file[21:29] + "_all_box_scores.csv", index=False)


def getBoxScoreIndex():
    array = pd.read_csv("DailyBoxScores/" + file[21:29] + "_all_box_scores.csv").to_numpy()
    team_abbreviations = ['MIL', 'PIT', 'CIN', 'PHI', 'ATL', 'WSH', 'BAL', 'BOS', 'CLE', 'DET', 'CHC', 'MIA', 'NYY',
                          'CHW', 'STL', 'KC', 'TB', 'MIN', 'OAK', 'TEX', 'COL', 'SF', 'HOU', 'LAA', 'SD', 'ARI', 'TOR',
                          'SEA', 'LAD', 'NYM']
    index = 0
    for i in range(0, len(array)):
        res = eval(array[i][0])
        date = str(list(res.values())[5][5:7] + list(res.values())[5][8:10] + list(res.values())[5][0:4])
        awayteam = list(res.values())[6]
        hometeam = list(res.values())[7]
        if date == file[21:29] and awayteam == file[29:31] and hometeam == file[31:33] and file[
                                                                                           29:31] in team_abbreviations and file[
                                                                                                                            31:33] in team_abbreviations:  ############# BOTH 2 LETTER ABBREVIATIONS
            return i

        elif date == file[21:29] and awayteam == file[29:31] and hometeam == file[31:34] and file[
                                                                                             29:31] in team_abbreviations and file[
                                                                                                                              31:34] in team_abbreviations:  ############# 2 THEN 3 LETTER ABBREVIATION
            return i
        elif date == file[21:29] and awayteam == file[29:32] and hometeam == file[32:34] and file[
                                                                                             29:32] in team_abbreviations and file[
                                                                                                                              32:34] in team_abbreviations:  ############# 3 THEN 2 LETTER ABBREVIATION
            return i

        elif date == file[21:29] and awayteam == file[29:32] and hometeam == file[32:35] and file[
                                                                                             29:32] in team_abbreviations and file[
                                                                                                                              32:35] in team_abbreviations:  ############# BOTH 3 LETTER ABBREVIATIONS
            return i


###CHANGE SCRAMBLED FLOAT###
def parseBoxScoretoPointsPerPlayer(index):
    array = pd.read_csv("ContestsOutput/" + file[21:29] + "_all_box_scores.csv").to_numpy()
    print(index)
    newarr = eval(array[index][3])
    playerstats = pd.DataFrame(newarr)
    columnslist = playerstats.columns
    # for i in columnslist:
    #     print(i)
    pd.DataFrame(newarr).to_csv(r"ContestsOutput/" + file[21:] + "_AFTER_GAME_player_stats.csv", index=False)
    newarr = pd.read_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_player_stats.csv").to_numpy()

    # SCORING FOR ONE GAME DFS: MVP, ALL-STAR, 3 NORMAL
    ### 1B = 3    2B = 6    3B = 9    HR = 12   BB = 3   HBP = 3   R = 3.2   RBI = 3.5   SB = 6
    ### 42         43       44         45       50        51        40         46         55

    playersandscores = []
    headers = ['Name', 'Singles', 'Doubles', 'Triples', 'Home Runs', 'Walks', 'HBP', 'R', 'RBI', 'SB', 'Points']
    for i in range(0, len(newarr)):
        name = str(newarr[i][5])
        for letter in range(0,
                            len(name)):  ### Adding player to new list without injuries and starting..... THIS IS THE SPECIAL CHARACTER FILTER FOR PLAYER NAMES
            if newarr[i][5][letter] == 'í':
                name = str(name[0:letter] + 'i' + name[letter + 1:])
            elif newarr[i][5][letter] == 'ú':
                name = str(name[0:letter] + 'u' + name[letter + 1:])
            elif newarr[i][5][letter] == 'á':
                name = str(name[0:letter] + 'a' + name[letter + 1:])
            elif newarr[i][5][letter] == 'ñ':
                name = str(name[0:letter] + 'n' + name[letter + 1:])
            elif newarr[i][5][letter] == 'é':
                name = str(name[0:letter] + 'e' + name[letter + 1:])

        player = name
        scrambledfloat = .6
        score = round(newarr[i][42] / scrambledfloat) * 3 + round(newarr[i][43] / scrambledfloat) * 6 + round(
            newarr[i][44] / scrambledfloat) * 9 + round(newarr[i][45] / scrambledfloat) * 12 + round(
            newarr[i][50] / scrambledfloat) * 3 + round(newarr[i][51] / scrambledfloat) * 3 + round(
            newarr[i][40] / scrambledfloat) * 3.2 + round(newarr[i][46] / scrambledfloat) * 3.5 + round(
            newarr[i][55] / scrambledfloat) * 6
        playersandscores.append(
            [newarr[i][5], round(newarr[i][42] / scrambledfloat), round(newarr[i][43] / scrambledfloat),
             round(newarr[i][44] / scrambledfloat), round(newarr[i][45] / scrambledfloat),
             round(newarr[i][50] / scrambledfloat), round(newarr[i][51] / scrambledfloat),
             round(newarr[i][40] / scrambledfloat), round(newarr[i][46] / scrambledfloat),
             round(newarr[i][55] / scrambledfloat), score])

    playersandscores.sort(key=lambda x: x[-1], reverse=True)
    pd.DataFrame(playersandscores).to_csv(r"ContestsOutput/" + file[21:] + "_AFTER_GAME_player_dfs_scores.csv",
                                          index=False, header=headers)


#########MAKE SURE BATTING ORDER IS COMPLETE
def addPlayerScoretoCSV():
    pl = pd.read_csv(file + ".csv", dtype=object).to_numpy()
    newarr = []
    for player in range(0, len(pl)):
        if (str(pl[player][11]) == 'nan') and (int(pl[player][15]) > 0):  #################### DUPLICATE FROM ABOVE, 1) save first list from above???? 2) filter by name 3) add scores to this second one too
            newarr.append(pl[player])

    for i in range(0,
                   len(newarr)):  ### Adding player to new list without injuries and starting..... THIS IS THE SPECIAL CHARACTER FILTER FOR PLAYER NAMES
        name = str(newarr[i][3])
        for letter in range(0, len(name)):
            if newarr[i][3][letter] == 'í':
                name = str(name[0:letter] + 'i' + name[letter + 1:])
            elif newarr[i][3][letter] == 'ú':
                name = str(name[0:letter] + 'u' + name[letter + 1:])
            elif newarr[i][3][letter] == 'á':
                name = str(name[0:letter] + 'a' + name[letter + 1:])
            elif newarr[i][3][letter] == 'ñ':
                name = str(name[0:letter] + 'n' + name[letter + 1:])
            elif newarr[i][3][letter] == 'é':
                name = str(name[0:letter] + 'e' + name[letter + 1:])

    pd.DataFrame(newarr).to_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_reduced_players_list.csv", index=False)

    array = pd.read_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_reduced_players_list.csv").to_numpy()
    array2 = pd.read_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_player_dfs_scores.csv").to_numpy()
    array = pd.DataFrame(array)
    array['DFS_Score'] = ""
    array = array.to_numpy()
    for i in range(0, len(array)):
        for j in range(0, len(array2)):
            if array[i][3] == array2[j][0]:
                array[i][-1] = array2[j][-1]
    pd.DataFrame(array).to_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_reduced_player_list_and_scores.csv",
                               index=False)


###FILTER OUTPUT ABILITY###
def editCombinationsWITHPlayerScores():
    array = pd.read_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_reduced_player_list_and_scores.csv").to_numpy()
    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11]) == 'nan') and (int(array[player][15]) > 0):
            newarray.append(array[player])

    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'SalaryTotal', 'PredictedDFSScore', 'ActualDFSScore']
    combos = list(permutations(newarray, 5))
    permutationsarr = []
    currentlineup = []
    predictedDFSScore = 0
    salary = 0
    salaryMax = 35000
    actualDFSScore = 0

    for combination in range(0, len(combos)):
        for player in range(0, len(combos[combination])):
            if (salary + combos[combination][player][7]) <= salaryMax:
                currentlineup.append(combos[combination][player][3])  # add player to current
                salary += combos[combination][player][7]  # add salary
                if player == 0:
                    predictedDFSScore += combos[combination][player][5] * 2  # MVP
                    if str(combos[combination][player][17]) == 'nan':
                        actualDFSScore += 0
                    else:
                        actualDFSScore += combos[combination][player][17] * 2
                elif player == 1:
                    predictedDFSScore += combos[combination][player][5] * 1.5  # STAR
                    if str(combos[combination][player][17]) == 'nan':
                        actualDFSScore += 0
                    else:
                        actualDFSScore += combos[combination][player][17] * 1.5
                else:
                    predictedDFSScore += combos[combination][player][5]  # NORMAL
                    if str(combos[combination][player][17]) == 'nan':
                        actualDFSScore += 0
                    else:
                        actualDFSScore += combos[combination][player][17]
            else:
                break

        if len(currentlineup) == 5:
            currentlineup.append(salary)
            currentlineup.append(predictedDFSScore)
            currentlineup.append(actualDFSScore)
            # print(currentlineup)
            permutationsarr.append(currentlineup)
        currentlineup = []
        salary = 0
        predictedDFSScore = 0
        actualDFSScore = 0

    newpermutationsarr = []  # removes the repition of every six entries being the same
    for i in range(6, len(permutationsarr) + 6):
        if i % 6 == 0:  # every sixth and lineup cost above 30000 ex. permutationsarr[i-6][5]>=30000  ####################### ADD FILTERS
            newpermutationsarr.append(permutationsarr[i - 6])
    newpermutationsarr.sort(key=lambda x: x[6], reverse=True)

    # check for all players team same and remove them
    players = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
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
        newpermutationsarr.pop(poplist[
                                   i] - pop_counter_deduction)  # needed to remove the proper array index after previous removal of elements
        pop_counter_deduction += 1
    # print(len(newpermutationsarr))
    # print(len(poplist))

    #save to csv
    pd.DataFrame(newpermutationsarr).to_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_permutations_with_scores.csv",
                                            index=False, header=headers)

    ###ADDING PERCENTILES
    x = pd.read_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_permutations_with_scores.csv")
    x['Predicted DFS Score Percentile Rank'] = x.PredictedDFSScore.rank(pct=True)
    x['Actual DFS Score Percentile Rank'] = x.ActualDFSScore.rank(pct=True)
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'SalaryTotal', 'PredictedDFSScore', 'ActualDFSScore',
               'Predicted DFS Score Percentile Rank', 'Actual DFS Score Percentile Rank']
    pd.DataFrame(x).to_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_permutations_with_scores_and_percentiles.csv",
                           index=False, header=headers)


########################################################################################################################
########################################   VISUALIZATION AND STATISTICS  ###############################################
########################################################################################################################
def seabornScatterplot():
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'SalaryTotal', 'PredictedDFSScore', 'ActualDFSScore',
               'Predicted DFS Score Percentile Rank', 'Actual DFS Score Percentile Rank']
    array = pd.read_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_permutations_with_scores_and_percentiles.csv")
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
    array = pd.read_csv("ContestsOutput/" + file[21:] + "_AFTER_GAME_permutations_with_scores_and_percentiles.csv")

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


def getDateFormatted():  # entered 01012021
    CalendarDict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                    "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    day = file[13:15]
    year = file[15:19]
    monthAbrev = CalendarDict[file[21:13]]
    x = str(year + '-' + monthAbrev + '-' + day)
    return x


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
            dfItem.to_csv(r"DailyBoxScores/" + str(
                str(current_date)[5:7] + str(current_date)[8:10] + str(current_date)[0:4]) + "_all_box_scores.csv",
                          index=False)
        current_date = current_date + datetime.timedelta(days=1)


def checkBoxScoresDirectory(current_date):
    directory = 'DailyBoxScores'
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


def moneyCalculationModule(entryfee, entries):
    array = pd.read_csv(
        "ContestsOutput/" + file[21:] + "_AFTER_GAME_permutations_with_scores_and_percentiles.csv").to_numpy()
    total = 0
    for i in range(0, 50):
        percentile = array[i][9]
        if percentile > 0.999378109:
            total += 1000
        elif percentile > 0.998756219:
            total += 500
        elif percentile > 0.998134328:
            total += 250
        elif percentile > 0.997512438:
            total += 125
        elif percentile > 0.996890547:
            total += 100
        elif percentile > 0.995646766:
            total += 75
        elif percentile > 0.993781095:
            total += 50
        elif percentile > 0.990671642:
            total += 40
        elif percentile > 0.987562189:
            total += 30
        elif percentile > 0.983830846:
            total += 20
        elif percentile > 0.975124378:
            total += 15
        elif percentile > 0.955845771:
            total += 12
        elif percentile > 0.928482587:
            total += 10
        elif percentile > 0.86318408:
            total += 9
        elif percentile > 0.763059701:
            total += 8
    print("Total Income: $" + str(total))
    print("Net Income: $" + str(total - (entryfee * entries)))


def graphVsIndex():
    # y_val_array = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineup_permutations.csv").to_numpy()
    # y_val = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineup_permutations.csv")
    y_val_array = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineups_selected.csv").to_numpy()
    y_val = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineups_selected.csv")
    x_val = []

    for i in range(0, len(y_val_array)):
        x_val.append(i)

    sns.scatterplot(x_val, y_val["LineupScore"], alpha=.1).set(
        title="Submission Lineup Rank vs. Predicted Outcome Score")

    sns.scatterplot(x_val, y_val["LineupScore"], alpha=.1).set(
        title="Submission Lineup Rank vs. Predicted Outcome Score")
    plt.show()


main()
