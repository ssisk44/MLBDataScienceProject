import pandas as pd
from itertools import permutations, combinations
import requests, time
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    seabornScatterplot()


### BEFORE GAME BEGINS
def getBoxScores(date):
    date = date
    response = requests.get("https://api.sportsdata.io/v3/mlb/stats/json/BoxScores/2021-Aug-09?key=86b4aafa44974957949c2312482b0f27")
    data = response.json()
    dfItem = pd.DataFrame.from_records(data)
    dfItem.to_csv(r'Aug92021BoxScores.csv', index=False)

def createCombinationsFromCSV():
    array = pd.read_csv('pl.csv').to_numpy()
    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11]) == 'nan') and (int(array[player][15]) > 0):
            newarray.append(array[player])

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
                    lineupscore += combos[combination][player][5] * 2.5  # MVP
                elif player == 1:
                    lineupscore += combos[combination][player][5] * 1.5  # STAR
                else:
                    lineupscore += combos[combination][player][5]  # NORMAL
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
    pd.DataFrame(permutationsarr).to_csv("permutations.csv", index=False)  # THIS IS FOR PERMUTATION TESTING




### AFTER GAME END
def parseBoxScoretoPointsPerPlayer():
    array = pd.read_csv('Aug92021BoxScores.csv').to_numpy()
    newarr = eval(array[4][3])
    playerstats = pd.DataFrame(newarr)
    # columnslist = playerstats.columns
    # for i in columnslist:
    #     print(i)
    pd.DataFrame(newarr).to_csv(r'Aug92021PlayerStats.csv', index=False)
    newarr = pd.read_csv('Aug92021PlayerStats.csv').to_numpy()

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
    pd.DataFrame(playersscorescheck).to_csv(r'Aug92021PlayerScoresCheck.csv', index=False, header=psc_headers)
    pd.DataFrame(playerandscores).to_csv(r'Aug92021PlayerScores.csv', index=False)

def addPlayerScoretoCSV():
    pl = pd.read_csv('pl.csv').to_numpy()
    newarray = []
    for player in range(0, len(pl)):
        if (str(pl[player][11]) == 'nan') and (int(pl[player][15]) > 0):
            newarray.append(pl[player])
    pd.DataFrame(newarray).to_csv("pl2_reduced.csv", index=False)

    array = pd.read_csv('pl2_reduced.csv').to_numpy()
    array2 = pd.read_csv('Aug92021PlayerScores.csv').to_numpy()
    array = pd.DataFrame(array)
    array['DFS_Score'] = ""
    array = array.to_numpy()
    for i in range(0, len(array)):
        for j in range(0, len(array2)):
            if array[i][3] == array2[j][0]:
                array[i][-1] = array2[j][1]
    pd.DataFrame(array).to_csv("pl3.csv", index=False)  # THIS IS FOR PERMUTATION TESTING

def editCombinationsWITHPlayerScores():
    array = pd.read_csv('pl3.csv').to_numpy()
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

    permutationsarr.sort(key=lambda x: x[7], reverse=True)
    pd.DataFrame(permutationsarr).to_csv("permsWScores.csv", index=False, header=headers)  # THIS IS FOR PERMUTATION TESTING

def seabornScatterplot():
    #['Name1','Name2','Name3','Name4','Name5','SalaryTotal','PredictedDFSScore','ActualDFSScore']
    array = pd.read_csv('permsWScores.csv')
    sns.scatterplot(array['PredictedDFSScore'], array['ActualDFSScore']).set(title="Predicted DFS Score vs. Actual DFS Score Outcome")
    plt.show()

    sns.scatterplot(array['SalaryTotal'], array['PredictedDFSScore']).set(title="Lineup Salary Total vs. Predicted DFS Score")
    plt.show()

    sns.scatterplot(array['SalaryTotal'], array['ActualDFSScore']).set(title="Lineup Salary Total vs. Actual DFS Score Outcome")
    plt.show()

main()
