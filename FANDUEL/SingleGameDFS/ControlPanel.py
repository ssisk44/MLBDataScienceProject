import datetime
import fnmatch
import math
import os
from statistics import mean
import scipy.stats as st
import numpy as np
import pandas as pd
from itertools import permutations, combinations
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import SingleGameDFSContestFunctions
from SingleGameDFSContestFunctions import file as THIS_IS_THE_FILE_NAME

def main():
    # createAllWiffleOutputFiles()
    # createOneWiffleOutputFile()
    # createAllOutputFiles()
    # getIndexofPlayerRanks()
    afterGameLineupCheck()


def createAllWiffleOutputFiles():
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/SingleGameContestCSVs/'
    contest_results = pd.read_csv('FanDuelContestRecordKeeping.csv')
    columns = []
    for col in contest_results:
        columns.append(col)
    wiffle_contest_results = contest_results[contest_results['ContestType'] == 'WIFFLE'].to_numpy()

    for i in range(0, len(wiffle_contest_results)):
        file = ('SingleGameContestCSVs/'+str(wiffle_contest_results[i][0]))
        game_date = SingleGameDFSContestFunctions.getDateFormattedtoDatetime(file[22:])
        game_date = str(str(game_date)[5:7] + str(game_date)[8:10] + str(game_date)[0:4])
        print("Checking: " + file[22:])
        if not str(file[22:] + '_AFTER_GAME_permutations_with_scores.csv') in os.listdir('C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/WIFFLE/'):
            if not (game_date + "_all_box_scores.csv") in os.listdir('C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores'):
                print("Box Not Score Found for: " + file)
                SingleGameDFSContestFunctions.getFileBoxScore(file[22:30])

            print("Creating Files for: " + file[22:])
            SingleGameDFSContestFunctions.createCombinationsFromCSV(0, file, "WIFFLE/")
            SingleGameDFSContestFunctions.parseBStoFPPG_addFPPGtoCSV_addSCOREStoCOMBOS(
            SingleGameDFSContestFunctions.getBoxScoreIndex(file), file, "WIFFLE/")

        else:
            print(file + ': OUTPUT FILES FOUND ---- not running DFS Contest Functions')
            continue
        print("Completed Files for: " + file[22:])
    print("\n DONE CREATING FILES \n")

def createOneWiffleOutputFile():
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/'
    wiffle_contests = getWiffleContests()
    permutation_files = []
    for file in os.listdir(directory):
        if "_AFTER_GAME_permutations_" in file:
            permutation_files.append(file)

    columns = []
    for col in pd.read_csv(directory + permutation_files[0]):
        columns.append(col)
    columns.append('ContestNumber')

    all_wiffle_array = []
    counter = 0
    for file in permutation_files:
        contest_results = pd.read_csv(directory + file)
        contest_results['ContestNumber'] = counter
        contest_results = contest_results.to_numpy()
        for i in range(0, len(contest_results)):
            all_wiffle_array.append(contest_results[i])
        counter+=1
    pd.DataFrame(all_wiffle_array).to_csv("ContestsOutput/ALLPERMUTATIONS.csv",index=False, header=columns)

def getWiffleContests():
    contest_results = pd.read_csv('FanDuelContestRecordKeeping.csv')
    columns = []
    for col in contest_results:
        columns.append(col)
    wiffle_contest_results = contest_results[contest_results['ContestType'] == 'WIFFLE']
    return wiffle_contest_results



def createAllOutputFiles():
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/SingleGameContestCSVs/'
    contest_results = pd.read_csv('FanDuelContestRecordKeeping.csv')
    columns = []
    for col in contest_results:
        columns.append(col)
    contest_results = contest_results.to_numpy()

    for i in range(0, len(contest_results)):
        file = ('SingleGameContestCSVs/'+str(contest_results[i][0]))
        game_date = SingleGameDFSContestFunctions.getDateFormattedtoDatetime(file[22:])
        game_date = str(str(game_date)[5:7] + str(game_date)[8:10] + str(game_date)[0:4])
        print("Checking: " + file[22:])
        if not str(file[22:] + '_AFTER_GAME_permutations_with_scores.csv') in os.listdir('C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/'):
            if not (game_date + "_all_box_scores.csv") in os.listdir('C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores'):
                print("Box Not Score Found for: " + file)
                SingleGameDFSContestFunctions.getFileBoxScore(file[22:30])

            print("Creating Files for: " + file[22:])
            SingleGameDFSContestFunctions.createCombinationsFromCSV(0, file, "ALL/")
            SingleGameDFSContestFunctions.parseBStoFPPG_addFPPGtoCSV_addSCOREStoCOMBOS(
            SingleGameDFSContestFunctions.getBoxScoreIndex(file), file, "ALL/")
        else:
            print(file + ': OUTPUT FILES FOUND ---- not running DFS Contest Functions \n')
            continue
        print("Completed Files for: " + file[22:] +'\n')
    print("\n DONE CREATING FILES \n")


def getIndexofPlayerRanks():
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/'

    MVP_index = []
    STAR_index = []
    UTIL1_index = []
    UTIL2_index = []
    UTIL3_index = []
    UTILALL_index = []

    for file in os.listdir(directory):
        if '_AFTER_GAME_reduced_player_list' in file:
            array = pd.read_csv(directory + file).to_numpy()
            for i in range(0, len(array)):
                if int(math.ceil(array[i][-1])) == 1:
                    MVP_index.append(i+1)
                elif int(math.ceil(array[i][-1])) == 2:
                    STAR_index.append(i+1)
                elif int(math.ceil(array[i][-1])) == 3:
                    UTIL1_index.append(i+1)
                    UTILALL_index.append(i+1)
                elif int(math.ceil(array[i][-1])) == 4:
                    UTIL2_index.append(i+1)
                    UTILALL_index.append(i + 1)
                elif int(math.ceil(array[i][-1])) == 5:
                    UTIL3_index.append(i+1)
                    UTILALL_index.append(i + 1)
    print(MVP_index)
    print(st.t.interval(alpha=0.99, df=len(MVP_index) - 1, loc=np.mean(MVP_index), scale=st.sem(MVP_index)))
    print('Index of MVP 99% Confidence\n')

    print(STAR_index)
    print(st.t.interval(alpha=0.99, df=len(STAR_index) - 1, loc=np.mean(STAR_index), scale=st.sem(STAR_index)))
    print('Index of STAR 99% Confidence\n')

    print(UTIL1_index)
    print(st.t.interval(alpha=0.99, df=len(UTIL1_index) - 1, loc=np.mean(UTIL1_index), scale=st.sem(UTIL1_index)))
    print('Index of UTIL1 99% Confidence\n')

    print(UTIL2_index)
    print(st.t.interval(alpha=0.99, df=len(UTIL2_index) - 1, loc=np.mean(UTIL2_index), scale=st.sem(UTIL2_index)))
    print('Index of UTIL2 99% Confidence\n')

    print(UTIL3_index)
    print(st.t.interval(alpha=0.99, df=len(UTIL3_index) - 1, loc=np.mean(UTIL3_index), scale=st.sem(UTIL3_index)))
    print('Index of UTIL3 99% Confidence\n')

    print(UTILALL_index)
    print(st.t.interval(alpha=0.99, df=len(UTILALL_index) - 1, loc=np.mean(UTILALL_index), scale=st.sem(UTILALL_index)))
    print('Index of 1 UTIL from all UTIL 99% Confidence\n')


def afterGameLineupCheck():
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/'

    contest_file = pd.read_csv('FanDuelContestRecordKeeping.csv')
    cuttoffscores = contest_file['WinningLineupCutoffScore'].to_numpy()
    games = contest_file['Game'].to_numpy()

    players = [0,1,2,3,4,5,6,7]
    combos = list(permutations(players, 2))

    total = [0,0]
    game_counter = 0
    for file in os.listdir(directory):
        players_scores = []
        if '_AFTER_GAME_reduced_player_list' in file:
            array = pd.read_csv(directory + file).to_numpy()
            for i in range(0, 8):
                players_scores.append(array[i][-2])
            for i in range(0,len(combos)):
                total[1] += 1
                score = players_scores[(combos[i][0])]*2 + players_scores[(combos[i][1])]*1.5
                if score >= cuttoffscores[game_counter]:
                    total[0] += 1

            game_counter+=1
    print(total[0])
    print(total[1])
    print("Percent of contests won by randomly guessing MVP, STAR from first 8 players ranked by fppg (no additional points): " + str(total[0]/total[1]*100))







main()