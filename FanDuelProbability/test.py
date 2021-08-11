import pandas as pd
from itertools import permutations, combinations
import requests, time
import seaborn as sns
import matplotlib.pyplot as plt

file = 'ContestCSV/08092021MIASDP.csv'
def main():
    ###PREGAME
    # createCombinationsFromCSV()
    # player_name_rank_counter()

    #POSTGAME
    # getBoxScores(time.time())
    # parseBoxScoretoPointsPerPlayer()
    # addPlayerScoretoCSV()
    editCombinationsWITHPlayerScores()






### BEFORE GAME BEGINS
def createCombinationsFromCSV():
    array = pd.read_csv(file).to_numpy()
    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11]) == 'nan') and (int(array[player][15]) > 0):
            newarray.append(array[player])
    pd.DataFrame(newarray).to_csv(str(file[0:12]) + "_reduced_players_list.csv", index=False)
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
                    lineupscore += float(combos[combination][player][5]) * 2.5  # MVP
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




    pd.DataFrame(newpermutationsarr).to_csv(str(file[0:12])+"permutations.csv", index=False)  # THIS IS FOR PERMUTATION TESTING

def player_name_rank_counter():
    permutations_array = pd.read_csv(str(file[0:12])+'permutations.csv').to_numpy()
    reduced_players_array = pd.read_csv(str(file[0:12]) + "_reduced_players_list.csv").to_numpy()
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

    pd.DataFrame(player_counter_array).to_csv(str(file[0:12]) + "player_lineup_disctribution.csv",
                                            index=False, header=headers)  # THIS IS FOR PERMUTATION TESTING



### AFTER GAME END
def getBoxScores(date):
    date = date
    response = requests.get("https://api.sportsdata.io/v3/mlb/stats/json/BoxScores/2021-Aug-09?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r'BoxScores.csv', index=False)

def parseBoxScoretoPointsPerPlayer():
    array = pd.read_csv('BoxScores.csv').to_numpy()
    newarr = eval(array[4][3])
    playerstats = pd.DataFrame(newarr)
    # columnslist = playerstats.columns
    # for i in columnslist:
    #     print(i)
    pd.DataFrame(newarr).to_csv(r'PlayerStats.csv', index=False)
    newarr = pd.read_csv('PlayerStats.csv').to_numpy()

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
        score = round(newarr[i][42]/1.4)*3 + round(newarr[i][43]/1.4)*6 + round(newarr[i][44]/1.4)*9 + round(newarr[i][45]/1.4)*12 + round(newarr[i][50]/1.4)*3 + round(newarr[i][51]/1.4)*3 + round(newarr[i][40]/1.4)*3.2 + round(newarr[i][46]/1.4)*3.5 + round(newarr[i][55]/1.4)*6
        playersscorescheck.append([newarr[i][5], round(newarr[i][42]/1.4), round(newarr[i][43]/1.4), round(newarr[i][44]/1.4), round(newarr[i][45]/1.4), round(newarr[i][50]/1.4), round(newarr[i][51]/1.4), round(newarr[i][40]/1.4), round(newarr[i][46]/1.4), round(newarr[i][55]/1.4)])
        playerandscores.append([player, score])
    playersscorescheck.sort(key=lambda x: x[2], reverse=True)
    pd.DataFrame(playersscorescheck).to_csv(r'PlayerScoresCheck.csv', index=False, header=psc_headers)
    pd.DataFrame(playerandscores).to_csv(r'PlayerScores.csv', index=False)

def addPlayerScoretoCSV():
    pl = pd.read_csv(file).to_numpy()
    newarray = []
    for player in range(0, len(pl)):
        if (str(pl[player][11]) == 'nan') and (int(pl[player][15]) > 0):
            newarray.append(pl[player])
    pd.DataFrame(newarray).to_csv("reduced_player_list.csv", index=False)

    array = pd.read_csv("reduced_player_list.csv").to_numpy()
    array2 = pd.read_csv('PlayerScores.csv').to_numpy()
    array = pd.DataFrame(array)
    array['DFS_Score'] = ""
    array = array.to_numpy()
    for i in range(0, len(array)):
        for j in range(0, len(array2)):
            if array[i][3] == array2[j][0]:
                array[i][-1] = array2[j][1]
    pd.DataFrame(array).to_csv("player_list_with_scores.csv", index=False)  # THIS IS FOR PERMUTATION TESTING

def editCombinationsWITHPlayerScores():
    array = pd.read_csv("player_list_with_scores.csv").to_numpy()
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
                    predictedDFSScore += combos[combination][player][5] * 2.5  # MVP
                    if str(combos[combination][player][17]) == 'nan':
                        actualDFSScore += 0
                    else:
                        actualDFSScore += combos[combination][player][17] * 2.5
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
        if i % 6 == 0:  # every sixth and lineup cost above 30000
            newpermutationsarr.append(permutationsarr[i - 6])
    newpermutationsarr.sort(key=lambda x: x[7], reverse=True)
    pd.DataFrame(newpermutationsarr).to_csv("permutations_with_scores.csv", index=False, header=headers)


    ###ADDING PERCENTILES
    x = pd.read_csv("permutations_with_scores.csv")
    x['Predicted DFS Score Percentile Rank'] = x.PredictedDFSScore.rank(pct=True)
    x['Actual DFS Score Percentile Rank'] = x.ActualDFSScore.rank(pct=True)
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'SalaryTotal', 'PredictedDFSScore', 'ActualDFSScore','Predicted DFS Score Percentile Rank','Actual DFS Score Percentile Rank']
    pd.DataFrame(x).to_csv("permutations_with_scores_and_percentiles.csv", index=False, header=headers)

def seabornScatterplot():
    #['Name1','Name2','Name3','Name4','Name5','SalaryTotal','PredictedDFSScore','ActualDFSScore']
    array = pd.read_csv(file+"permutations_with_scores.csv")
    sns.scatterplot(array['PredictedDFSScore'], array['ActualDFSScore']).set(title="Predicted DFS Score vs. Actual DFS Score Outcome")
    plt.show()

    sns.scatterplot(array['SalaryTotal'], array['PredictedDFSScore']).set(title="Lineup Salary Total vs. Predicted DFS Score")
    plt.show()

    sns.scatterplot(array['SalaryTotal'], array['ActualDFSScore']).set(title="Lineup Salary Total vs. Actual DFS Score Outcome")
    plt.show()

main()
