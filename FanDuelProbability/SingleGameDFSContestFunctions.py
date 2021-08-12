import datetime
import pandas as pd
from itertools import permutations, combinations
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import ast

file = 'ContestCSV/08102021TORLAA'
def main():
    # ###PREGAME
    # createCombinationsFromCSV()
    # player_name_rank_counter()
    #
    # ###POSTGAME
    # getAllBoxScores()
    # parseBoxScoretoPointsPerPlayer(getBoxScoreIndex())
    # addPlayerScoretoCSV()
    editCombinationsWITHPlayerScores()
    #seabornScatterplot()
    moneyCalculationModule(4.44,50)





########################################################################################################################
#################################################### BEFORE GAME #######################################################
########################################################################################################################

def createCombinationsFromCSV():
    array = pd.read_csv(file+".csv").to_numpy()
    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11]) == 'nan') and (int(array[player][15]) > 0):
            newarray.append(array[player])
    pd.DataFrame(newarray).to_csv("ContestsOutput/"+str(file[11:]) + "_reduced_players_list.csv", index=False)
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

    newpermutationsarr = [] #removes the repition of every six entries being the same
    for i in range(6, len(permutationsarr)+6):
        if i%6==0 and permutationsarr[i-6][5]>=35000 and permutationsarr[i-6][6]>=60: #every sixth and lineup cost above 30000
            newpermutationsarr.append(permutationsarr[i-6])


    pd.DataFrame(newpermutationsarr).to_csv("ContestsOutput/"+file[11:] + "_before_game_lineup_permutations.csv", index=False)  # THIS IS FOR PERMUTATION TESTING

def player_name_rank_counter():
    permutations_array = pd.read_csv("ContestsOutput/"+file[11:] + "_before_game_lineup_permutations.csv").to_numpy()
    reduced_players_array = pd.read_csv("ContestsOutput/"+file[11:] + "_reduced_players_list.csv").to_numpy()
    player_counter_array = []
    headers = ['Player Name', "# of MVPs", "# of All Stars", "# of Regulars"]



    for name in range(0,len(reduced_players_array)):
        player_counter_array.append([reduced_players_array[name][3],0,0,0])


    for i in range(0, len(permutations_array)):
        for j in range(0, len(player_counter_array)):
            for k in range(0, 5):

                if permutations_array[i][k] == player_counter_array[j][0]:
                    if k==0:
                        player_counter_array[j][1] += 1
                    if k==1:
                        player_counter_array[j][2] += 2
                    if k==2 or k==3 or k==4:
                        player_counter_array[j][3] += 3

    pd.DataFrame(player_counter_array).to_csv("ContestsOutput/"+file[11:] + "_before_game_player_created_lineups_distributions.csv",
                                            index=False, header=headers)  # THIS IS FOR PERMUTATION TESTING




########################################################################################################################
################################################## AFTER GAME ENDS #####################################################
########################################################################################################################
def getAllBoxScores():
    response = requests.get('https://api.sportsdata.io/v3/mlb/stats/json/BoxScores/'+str(getDateFormatted())+'?key=86b4aafa44974957949c2312482b0f27')
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r"ContestsOutput/"+file[11:] + "_retrieved_all_box_scores.csv", index=False)

###MAKE SURE TEAM ABBREVS ARE CORRECT
def getBoxScoreIndex():
    array = pd.read_csv("ContestsOutput/" + file[11:] + "_retrieved_all_box_scores.csv").to_numpy()
    index = 0
    for i in range(0,len(array)):
        res = eval(array[i][0])
        date = str(list(res.values())[5][5:7] + list(res.values())[5][8:10] + list(res.values())[5][0:4])
        awayteam = list(res.values())[6]
        hometeam = list(res.values())[7]
        if date == file[11:19] and awayteam == file[19:22] and hometeam == file[22:]:  ############# MAY CAHNGE DEPENDING ON TEAM NAME
           return i

###CHANGE SCRAMBLED FLOAT###
def parseBoxScoretoPointsPerPlayer(index):
    array = pd.read_csv("ContestsOutput/"+file[11:] + "_retrieved_all_box_scores.csv").to_numpy()
    newarr = eval(array[index][3])
    playerstats = pd.DataFrame(newarr)
    columnslist = playerstats.columns
    # for i in columnslist:
    #     print(i)
    pd.DataFrame(newarr).to_csv(r"ContestsOutput/"+file[11:] + "_after_game_player_stats.csv", index=False)
    newarr = pd.read_csv("ContestsOutput/"+file[11:] + "_after_game_player_stats.csv").to_numpy()

    # SCORING FOR ONE GAME DFS: MVP, ALL-STAR, 3 NORMAL
    ### 1B = 3    2B = 6    3B = 9    HR = 12   BB = 3   HBP = 3   R = 3.2   RBI = 3.5   SB = 6
    ### 42         43       44         45       50        51        40         46         55
    playerandscores = []
    playersscorescheck = []
    psc_headers = ['Name','Singles','Doubles','Triples','Home Runs', 'Walks', 'HBP','R','RBI','SB']
    for i in range(0, len(newarr)):
        name = str(newarr[i][5])
        for letter in range(0, len(name)): ### Adding player to new list without injuries and starting..... THIS IS THE SPECIAL CHARACTER FILTER FOR PLAYER NAMES
            if newarr[i][5][letter] == 'í':
                name = str(name[0:letter]+'i'+name[letter+1:])
            elif newarr[i][5][letter] == 'ú':
                name = str(name[0:letter]+'u'+name[letter+1:])
            elif newarr[i][5][letter] == 'á':
                name = str(name[0:letter]+'a'+name[letter+1:])
            elif newarr[i][5][letter] == 'ñ':
                name = str(name[0:letter]+'n'+name[letter+1:])

        player = name
        scrambledfloat = 1.6
        score = round(newarr[i][42]/scrambledfloat)*3 + round(newarr[i][43]/scrambledfloat)*6 + round(newarr[i][44]/scrambledfloat)*9 + round(newarr[i][45]/scrambledfloat)*12 + round(newarr[i][50]/scrambledfloat)*3 + round(newarr[i][51]/scrambledfloat)*3 + round(newarr[i][40]/scrambledfloat)*3.2 + round(newarr[i][46]/scrambledfloat)*3.5 + round(newarr[i][55]/scrambledfloat)*6
        playersscorescheck.append([newarr[i][5], round(newarr[i][42]/scrambledfloat), round(newarr[i][43]/scrambledfloat), round(newarr[i][44]/scrambledfloat), round(newarr[i][45]/scrambledfloat), round(newarr[i][50]/scrambledfloat), round(newarr[i][51]/scrambledfloat), round(newarr[i][40]/scrambledfloat), round(newarr[i][46]/scrambledfloat), round(newarr[i][55]/scrambledfloat)])
        playerandscores.append([player, score])
    playersscorescheck.sort(key=lambda x: x[2], reverse=True)
    pd.DataFrame(playersscorescheck).to_csv(r"ContestsOutput/"+file[11:] + "_after_game_necessary_player_stats_retrieved.csv", index=False, header=psc_headers)
    pd.DataFrame(playerandscores).to_csv(r"ContestsOutput/"+file[11:] + "_after_game_player_dfs_scores.csv", index=False)

def addPlayerScoretoCSV(): #########MAKE SURE BATTING ORDER IS COMPLETE
    pl = pd.read_csv(file+".csv", dtype=object).to_numpy()
    newarray = []
    for player in range(0, len(pl)):
        if (str(pl[player][11]) == 'nan') and (int(pl[player][15]) > 0):  ####################
            newarray.append(pl[player])
    pd.DataFrame(newarray).to_csv("ContestsOutput/"+file[11:] + "_reduced_players_list.csv", index=False)

    array = pd.read_csv("ContestsOutput/"+file[11:] + "_reduced_players_list.csv").to_numpy()
    array2 = pd.read_csv("ContestsOutput/"+file[11:] + "_after_game_player_dfs_scores.csv").to_numpy()
    array = pd.DataFrame(array)
    array['DFS_Score'] = ""
    array = array.to_numpy()
    for i in range(0, len(array)):
        for j in range(0, len(array2)):
            if array[i][3] == array2[j][0]:
                array[i][-1] = array2[j][1]
    pd.DataFrame(array).to_csv("ContestsOutput/"+file[11:] + "_after_game_scores_added_to_reduced_player_list.csv", index=False)

###FILTER OUTPUT ABILITY###
def editCombinationsWITHPlayerScores():
    array = pd.read_csv("ContestsOutput/"+file[11:] + "_after_game_scores_added_to_reduced_player_list.csv").to_numpy()
    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11]) == 'nan') and (int(array[player][15]) > 0):
            newarray.append(array[player])

    headers = ['Name1','Name2','Name3','Name4','Name5','SalaryTotal','PredictedDFSScore','ActualDFSScore']
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
    newpermutationsarr.sort(key=lambda x: x[7], reverse=True)
    pd.DataFrame(newpermutationsarr).to_csv("ContestsOutput/"+file[11:] + "_after_game_permutations_with_scores.csv", index=False, header=headers)


    ###ADDING PERCENTILES
    x = pd.read_csv("ContestsOutput/"+file[11:] + "_after_game_permutations_with_scores.csv")
    x['Predicted DFS Score Percentile Rank'] = x.PredictedDFSScore.rank(pct=True)
    x['Actual DFS Score Percentile Rank'] = x.ActualDFSScore.rank(pct=True)
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'SalaryTotal', 'PredictedDFSScore', 'ActualDFSScore','Predicted DFS Score Percentile Rank','Actual DFS Score Percentile Rank']
    pd.DataFrame(x).to_csv("ContestsOutput/"+file[11:] + "_after_game_permutations_with_scores_and_percentiles.csv", index=False, header=headers)

def seabornScatterplot():
    headers = ['Name1','Name2','Name3','Name4','Name5','SalaryTotal','PredictedDFSScore','ActualDFSScore','Predicted DFS Score Percentile Rank','Actual DFS Score Percentile Rank']
    array = pd.read_csv("ContestsOutput/"+file[11:] + "_after_game_permutations_with_scores_and_percentiles.csv")
    array = array[array['SalaryTotal'] >= 00000]
    array = array[array['Actual DFS Score Percentile Rank'] >= .750000000000000000]
    print(len(array))

    # sns.scatterplot(array['Actual DFS Score Percentile Rank'], array['ActualDFSScore'], array['SalaryTotal'],alpha=.1).set(title="Predicted DFS Percentile vs. Actual DFS Score Outcome")
    # plt.show()

    # sns.scatterplot(array['Actual DFS Score Percentile Rank'], array['Predicted DFS Score Percentile Rank'], array['SalaryTotal'], alpha=1).set(title="Predicted DFS Percentile vs. Actual DFS Score Outcome")
    # plt.show()


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

def getDateFormatted():  #entered 01012021
    CalendarDict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul",
                    "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    day = file[13:15]
    year = file[15:19]
    monthAbrev = CalendarDict[file[11:13]]
    x = str(year + '-' + monthAbrev + '-' + day)
    return x

def moneyCalculationModule(entryfee,entries):
    array = pd.read_csv(
        "ContestsOutput/" + file[11:] + "_after_game_permutations_with_scores_and_percentiles.csv").to_numpy()
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
    print("Net Income: $" + str(total-(entryfee*entries)))


main()
