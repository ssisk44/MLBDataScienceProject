import datetime
import fnmatch
import os
from statistics import mean
import pandas as pd
from itertools import permutations, combinations
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import SingleGameDFSContestFunctions
from SingleGameDFSContestFunctions import file as THIS_IS_THE_FILE_NAME

def main():
    createAllWiffleOutputFiles()




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
        if not str(file[22:] + '_AFTER_GAME_permutations_with_scores.csv') in os.listdir('C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/'):
            if not (game_date + "_all_box_scores.csv") in os.listdir('C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores'):
                print("Box Not Score Found for: " + file)
                SingleGameDFSContestFunctions.getFileBoxScore(file[22:30])

            print("Creating Files for: " + file[22:])
            SingleGameDFSContestFunctions.createCombinationsFromCSV(30000, file)
            SingleGameDFSContestFunctions.parseBStoFPPG_addFPPGtoCSV_addSCOREStoCOMBOS(
            SingleGameDFSContestFunctions.getBoxScoreIndex(file), file)

        else:
            print(file + ': OUTPUT FILES FOUND ---- not running DFS Contest Functions')
            continue
    print("\n DONE CREATING FILES \n")













main()