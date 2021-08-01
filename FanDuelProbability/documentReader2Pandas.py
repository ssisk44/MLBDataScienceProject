import pandas as pd
import numpy as np
import time

salaryMax = 35000
injuryPruning = ['DTD', 'IL']
listIndices = ['Id', 'Position', 'First Name', 'Nickname', 'Last Name', 'FPPG', 'Played', 'Salary', 'Game', 'Team',
               'Opponent', 'Injury Indicator', 'Injury Details', 'Tier', 'Probable Pitcher', 'Batting Order',
               'Roster Position',"# of Lineups In", "Lineup AVG fantasy score"]
playerfiles = ["PitcherOUT.csv",'CatcherAndFirstOUT.csv',"SecondOUT.csv","ThirdOUT.csv","ShortstopOUT.csv","OutfielderOUT.csv","UtilityOUT.csv"]

def main():
    #readfile()
    start = time.time()
    createLineup()
    end = time.time()
    print("TOTAL RUN TIME: ", end-start)

def readfile():
    file = 'ContestCSV/073021Squeeze.csv'
    df = pd.read_csv(file)
    array = df.to_numpy()

    AlreadyAddedUtil = []
    Pitcher_arr = []
    CatcherAndFirst_arr = []
    Second_arr = []
    Shortstop_arr = []
    Third_arr = []
    Outfielder_arr = []
    Utility_arr = []

    for player in array:
        if str(player[11]) == 'nan':
            if 'P' in str(player[1]) and str(player[14]) == 'Yes':
                Pitcher_arr.append(player)
            if ('C' in str(player[1]) or '1B' in str(player[1])) and player[15] != 0 and int(player[5])>5:
                CatcherAndFirst_arr.append(player)
                if player[0] not in AlreadyAddedUtil:
                    Utility_arr.append(player)
                    AlreadyAddedUtil.append(player[0])
            if '2B' in str(player[1]) and player[15] != 0 and int(player[5])>5:
                Second_arr.append(player)
                if player[0] not in AlreadyAddedUtil:
                    Utility_arr.append(player)
                    AlreadyAddedUtil.append(player[0])
            if 'SS' in str(player[1]) and player[15] != 0 and int(player[5])>5:
                Shortstop_arr.append(player)
                if player[0] not in AlreadyAddedUtil:
                    Utility_arr.append(player)
                    AlreadyAddedUtil.append(player[0])
            if '3B' in str(player[1]) and player[15] != 0 and int(player[5])>5:
                Third_arr.append(player)
                if player[0] not in AlreadyAddedUtil:
                    Utility_arr.append(player)
                    AlreadyAddedUtil.append(player[0])
            if 'OF' in str(player[1]) and player[15] != 0 and int(player[5])>5:
                Outfielder_arr.append(player)
                if player[0] not in AlreadyAddedUtil:
                    Utility_arr.append(player)
                    AlreadyAddedUtil.append(player[0])

    Pitcher_arr = np.asarray(Pitcher_arr)
    CatcherAndFirst_arr = np.asarray(CatcherAndFirst_arr)
    Second_arr = np.asarray(Second_arr)
    Shortstop_arr = np.asarray(Shortstop_arr)
    Third_arr = np.asarray(Third_arr)
    Outfielder_arr = np.asarray(Outfielder_arr)
    Utility_arr = np.asarray(Utility_arr)

    numpylist = [Pitcher_arr, CatcherAndFirst_arr, Second_arr, Third_arr, Shortstop_arr, Outfielder_arr, Utility_arr]
    csvnameslist = ['PitcherOUT.csv', 'CatcherAndFirstOUT.csv', 'SecondOUT.csv', 'ThirdOUT.csv', 'ShortstopOUT.csv', 'OutfielderOUT.csv', 'UtilityOUT.csv']

    for i in range(0, len(numpylist)):
        size = numpylist[i].shape
        numEntries = size[0]
        newColumns = np.zeros((numEntries, 2))
        new_array = np.append(numpylist[i], newColumns, 1)
        pd.DataFrame(new_array).to_csv("PositionsCSV/" + csvnameslist[i], index=False)

def createLineup():
    Pitcher = pd.read_csv("PositionsCSV/PitcherOUT.csv").to_numpy()
    CatcherAndFirst = pd.read_csv("PositionsCSV/CatcherAndFirstOUT.csv").to_numpy()
    Second = pd.read_csv("PositionsCSV/SecondOUT.csv").to_numpy()
    Third = pd.read_csv("PositionsCSV/ThirdOUT.csv").to_numpy()
    Shortstop = pd.read_csv("PositionsCSV/ShortstopOUT.csv").to_numpy()
    Outfielder = pd.read_csv("PositionsCSV/OutfielderOUT.csv").to_numpy()
    Utility = pd.read_csv("PositionsCSV/UtilityOUT.csv").to_numpy()

    digit = Pitcher.shape[0]+Utility.shape[0]
    PitcherNames = []
    BatterNames = []
    for i in Pitcher:
        PitcherNames.append(i[3])
    for i in Utility:
        BatterNames.append(i[3])
    Names = PitcherNames + BatterNames

    NamesLineupsAVGlist = []

    for i in range(0,len(Names)):
        NamesLineupsAVGlist.append([Names[i],0,0])
    NamesLineupsAVGarray = np.array(NamesLineupsAVGlist,dtype=object)

    def adjust(index, avg):
        NamesLineupsAVGarray[index][1] += 1
        if NamesLineupsAVGarray[index][1] == 1:
            NamesLineupsAVGarray[index][2] = avg
        else:
            NamesLineupsAVGarray[index][2] = (((NamesLineupsAVGarray[index][1] - 1) * NamesLineupsAVGarray[index][2]) + avg)/NamesLineupsAVGarray[index][1]
        # print(NamesLineupsAVGarray[index][0], " Average = ", NamesLineupsAVGarray[index][2])

    permustationsList = [] #THIS IS FOR PERMUTATION TESTING
    currentList = []
    for p in range(0, len(Pitcher)):
        currentList.append(p)

        for CnOne in range(0, len(CatcherAndFirst)):
            if ((Pitcher[p][7]+CatcherAndFirst[CnOne][7]) > salaryMax-(2000*7)) or (CnOne in currentList):
                continue
            currentList.append(CnOne)

            for se in range(0, len(Second)):
                if ((Pitcher[p][7]+CatcherAndFirst[CnOne][7]+Second[se][7]) > salaryMax-(2000*6)) or (se in currentList):
                    continue
                currentList.append(se)

                # permustationsList.append([Pitcher[p][3], CatcherAndFirst[CnOne][3], Second[se][3]]) THIS IS FOR PERMUTATION TESTING
                # AvgScore = (Pitcher[p][5] + CatcherAndFirst[CnOne][5] + Second[se][5])/2

                for t in range(0, len(Third)):
                    if ((Pitcher[p][7]+CatcherAndFirst[CnOne][7]+Third[t][7]) > salaryMax-(2000*5)) or (t in currentList):
                        continue
                    currentList.append(t)

                    for ss in range(0, len(Shortstop)):
                        if ((Pitcher[p][7]+CatcherAndFirst[CnOne][7]+Third[t][7]+Shortstop[ss][7]) > salaryMax-(2000*4)) or (ss in currentList):
                            continue
                        currentList.append(ss)

                        for u in range(0, len(Utility)):
                            if ((Pitcher[p][7]+CatcherAndFirst[CnOne][7]+Second[se][7]+Third[t][7]+Shortstop[ss][7]+Utility[u][7]) > salaryMax-(2000*3)) or (u in currentList):
                                continue
                            currentList.append(u)
                            AvgScore = (Pitcher[p][5] + CatcherAndFirst[CnOne][5] + Second[se][5] + Third[t][5] +
                                        Shortstop[ss][5] + Utility[u][5]) / 6
                            for j in range(0, len(NamesLineupsAVGarray)):
                                if Pitcher[p][3] == NamesLineupsAVGarray[j][0]:
                                    adjust(j, AvgScore)
                                elif CatcherAndFirst[CnOne][3] == NamesLineupsAVGarray[j][0]:
                                    adjust(j, AvgScore)
                                elif Second[se][3] == NamesLineupsAVGarray[j][0]:
                                    adjust(j, AvgScore)
                                elif Third[t][3] == NamesLineupsAVGarray[j][0]:
                                    adjust(j, AvgScore)
                                elif Shortstop[ss][3] == NamesLineupsAVGarray[j][0]:
                                    adjust(j, AvgScore)
                                elif Utility[u][3] == NamesLineupsAVGarray[j][0]:
                                    adjust(j, AvgScore)
                            permustationsList.append([Pitcher[p][3], CatcherAndFirst[CnOne][3], Second[se][3], Third[t][3], Shortstop[ss][3], Utility[u][3]])
                            currentList = []  # MAKE SURE YOU RESET ARRAY AT THE END
                        #
                        #
                        #
                        #     for of1 in range(0, len(Outfielder)):
                        #         if(Pitcher[p][7] + CatcherAndFirst[CnOne][7] + Second[se][7] + Third[t][7] + Shortstop[ss][7] + Utility[u][7] + Outfielder[of1][7] > salaryMax-(2000*2)) or (of1 in currentList):
                        #             continue
                        #         currentList.append(of1)
                        #
                        #         for of2 in range(0, len(Outfielder)):
                        #             if (Pitcher[p][7] + CatcherAndFirst[CnOne][7] + Second[se][7] + Third[t][7] + Shortstop[ss][7] + Utility[u][7] + Outfielder[of1][7] > salaryMax - (2000)) or (of2 in currentList):
                        #                 continue
                        #             currentList.append(of2)
                        #             print(currentList)
                        #
                        #             for of3 in range(0, len(Outfielder)):
                        #                 if((Pitcher[p][7] + CatcherAndFirst[CnOne][7] + Second[se][7] + Third[t][7] + Shortstop[ss][7] + Utility[u][7] + Outfielder[of1][7] + Outfielder[of2][7] + Outfielder[of3][7]) > salaryMax) or (of3 in currentList):
                        #                     continue
                        #                 currentList.append(of3)
                        #
                        #                 AvgScore = (Pitcher[p][5] + CatcherAndFirst[CnOne][5] + Second[se][5] + Third[t][5] + Shortstop[ss][5] + Utility[u][5] + Outfielder[of1][5] + Outfielder[of2][5] + Outfielder[of3][5])/9
                        #                 for j in range(0, len(NamesLineupsAVGarray)):
                        #      for of1 in range(0, len(Outfielder)):
                        #          for of2 in range(0, len(Outfielder)):
                        #              for of3 in range(0, len(Outfielder)):
                        #                  if((Pitcher[p][7] + CatcherAndFirst[CnOne][7] + Second[se][7] + Third[t][7] + Shortstop[ss][7] + Utility[u][7] + Outfielder[of1][7] + Outfielder[of2][7] + Outfielder[of3][7]) > salaryMax) or (of3 in currentList):
                        #                         #                     continue

                        #                     if Pitcher[p][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif CatcherAndFirst[CnOne][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif Second[se][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif Third[t][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif Shortstop[ss][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif Utility[u][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif Outfielder[of1][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif Outfielder[of2][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                     elif Outfielder[of3][3] == NamesLineupsAVGarray[j][0]:
                        #                         adjust(j, AvgScore)
                        #                 currentList = []  # MAKE SURE YOU RESET ARRAY AT THE END





    pd.DataFrame(permustationsList).to_csv("PositionsCSV/permutations.csv", index=False) #THIS IS FOR PERMUTATION TESTING
    pd.DataFrame(NamesLineupsAVGarray).to_csv("PositionsCSV/NLAVG", index=False)




main()
