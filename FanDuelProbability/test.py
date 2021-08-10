import pandas as pd
from itertools import permutations, combinations


def main():
    createCombinationsFromCSV()


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


main()
