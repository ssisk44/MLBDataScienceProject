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
from keras.losses import mean_squared_error, mean_absolute_error
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def main():
    # createAllWiffleOutputFiles()
    # createOneWiffleOutputFile()
    # createAllOutputFiles()
    # getIndexofPlayerRanks()
    # afterGameLineupCheck()
    # createOneMVPSTAROutputFile()
    # MLTIME()
    # permutationsStatistics()
    # ML2()
    makeSubmission()




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
                print("Fetching Box Score")
                SingleGameDFSContestFunctions.getFileBoxScore(file[22:30])

            print("Creating Files for: " + file[22:])
            SingleGameDFSContestFunctions.createCombinationsFromCSV(0, file, "WIFFLE/")
            SingleGameDFSContestFunctions.parseBStoFPPG_addFPPGtoCSV_addSCOREStoCOMBOS(
            SingleGameDFSContestFunctions.getBoxScoreIndex(file), file, "WIFFLE/")

        else:
            print(file + ': OUTPUT FILES FOUND ---- not running DFS Contest Functions\n')
            continue
        print("Completed Files for: " + file[22:]+'\n')
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
        if '_AFTER_GAME_reduced_player_list_with_scores' in file:
            array = pd.read_csv(directory + file).to_numpy()
            for i in range(0, len(array)):
                if int(math.ceil(array[i][-1])) == 1:
                    MVP_index.append(i)
                elif int(math.ceil(array[i][-1])) == 2:
                    STAR_index.append(i)
                elif int(math.ceil(array[i][-1])) == 3:
                    UTIL1_index.append(i)
                    UTILALL_index.append(i)
                elif int(math.ceil(array[i][-1])) == 4:
                    UTIL2_index.append(i)
                    UTILALL_index.append(i)
                elif int(math.ceil(array[i][-1])) == 5:
                    UTIL3_index.append(i)
                    UTILALL_index.append(i)
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
    columns = []
    contest_file = pd.read_csv('FanDuelContestRecordKeeping.csv')
    for col in contest_file:
        columns.append(col)
    cuttoffscores = contest_file['WinningLineupCutoffScore'].to_numpy()
    games = contest_file['Game'].to_numpy()

    players = [0,1,2,3,4,5,6,7]
    combos = list(permutations(players, 2))

    total = [0,0]
    game_counter = 0
    for file in os.listdir(directory):
        players_scores = []

        if '_AFTER_GAME_reduced_player_list' in file: #calculated score just based off of MLB and STAR
            array = pd.read_csv(directory + file).to_numpy()
            for i in range(0, 8):
                players_scores.append(array[i][-2])
            for i in range(0,len(combos)):
                total[1] += 1
                score = players_scores[(combos[i][0])]*2 + players_scores[(combos[i][1])]*1.5
                if score >= cuttoffscores[game_counter]:
                    total[0] += 1
            game_counter += 1

        if '_AFTER_GAME_permutations_with_scores' in file: #gets all permutations that match the selected 56 combos
            permutations_ = pd.read_csv(directory + file)
            columns_new = []
            for col in permutations_:
                columns_new.append(col)

            permutations_ = permutations_.to_numpy()

            newpermutations = []
            for i in range(0, len(permutations_)):
                for j in range(0, len(combos)):
                    for k in range(0, 2):
                        if permutations_[i][7] == combos[j][0] and permutations_[i][8] == combos[j][1]:
                            newpermutations.append(permutations_[i])

            pd.DataFrame(newpermutations).to_csv("ContestsOutput/ALL/"+file[:getFileLength(file)]+"_AFTER_GAME_mvp_star_permutations.csv", index=False, header=columns_new)

    print("Percent of contests won by randomly guessing MVP, STAR from first 8 players ranked by fppg (no additional points): " + str(total[0]/total[1]*100) + '\n')

def createOneMVPSTAROutputFile():
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/'

    permutation_files = []
    for file in os.listdir(directory):
        if "_AFTER_GAME_mvp_star_permutations" in file:
            permutation_files.append(file)

    columns = []
    for col in pd.read_csv(directory + str(permutation_files[0])):
        columns.append(col)

    all_ALL_array = []
    for file in permutation_files:
        contest_results = pd.read_csv(directory + file).to_numpy()
        for i in range(0, len(contest_results)):
            all_ALL_array.append(contest_results[i])

    pd.DataFrame(all_ALL_array).to_csv("ContestsOutput/ALLMVPSTARPERMUTATIONS.csv", index=False, header=columns)
    print(len(all_ALL_array))

def getFileLength(string):
    return string.find('_')


def permutationsStatistics():
    df = pd.read_csv('C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALLMVPSTARPERMUTATIONS.csv')
    df = df[df['Actual DFS Score Percentile Rank']>=.9000]
    meanmeanBO = df['LineupMeanBattingOrder'].mean()
    minmeanBO = df['LineupMeanBattingOrder'].min()
    maxmeanBO = df['LineupMeanBattingOrder'].max()
    meanmeanRank = df['LineupMeanRank'].mean()
    minmeanRank = df['LineupMeanRank'].min()
    maxmeanRank = df['LineupMeanRank'].max()
    meanmeanSalary = df['Salary'].mean()
    minmeanSalary = df['Salary'].min()
    maxmeanSalary = df['Salary'].max()
    print("Batting Order Mean Min Max", meanmeanBO, minmeanBO, maxmeanBO)
    print("Rank Mean Min Max", meanmeanRank, minmeanRank, maxmeanRank)
    print("Salary Mean Min Max", meanmeanSalary, minmeanSalary, maxmeanSalary)
    columns = []
    for col in df:
        columns.append(col)


    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/'
    selections = []
    for file in os.listdir(directory):
        if '_BEFORE_GAME_lineup_permutations' in file:
            permutations_arr = pd.read_csv(directory + file).to_numpy()
            print(file)
            comboslist = [0,1,2,3,4,5,6,7]
            combos = list(permutations(comboslist,2))

            combos_permutations_match = []
            for i in range(0,len(combos)):


                for j in range(0,len(permutations_arr)):
                    if permutations_arr[j][7] == combos[i][0] and permutations_arr[j][8] == combos[i][1]:
                        combos_permutations_match.append(permutations_arr[j])



                df = pd.DataFrame(combos_permutations_match, columns=columns)
                s = ML2(df)
                for i in s:
                    selections.append(i)
            break
    pd.DataFrame(selections).to_csv(directory+'test/'+str('hi.csv'), index=False, header=columns)










            #     print(combos[i], len(combos_permutations_match))
            # print('\n')

def makeSubmission():
    directory = 'C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/08252021LADSD_BEFORE_GAME_lineup_permutations.csv'
    ML2(directory)
    directory='C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/test/killme.csv'

    permutations_arr = pd.read_csv(directory)
    selected_features_x = ['Salary', 'Player1Rank', 'Player2Rank', 'Player3Rank', 'Player4Rank', 'Player5Rank',
                           'LineupMeanRank', 'Player1BattingOrder', 'Player2BattingOrder', 'Player3BattingOrder',
                           'Player4BattingOrder', 'Player5BattingOrder', 'LineupMeanBattingOrder',
                           'Predicted DFS Score Percentile Rank', 'Prediction']
    permutations_arr = permutations_arr[selected_features_x]
    permutations_arr = permutations_arr.to_numpy()

    comboslist = [0,1,2,3,4,5,6,7]
    combos = list(permutations(comboslist,2))

    selections = []
    counter = 0
    all_counter = 0
    for i in range(0,len(combos)):
        combos_permutations_match = []

        for j in range(0,len(permutations_arr)):
            if permutations_arr[j][1] == combos[i][0] and permutations_arr[j][2] == combos[i][1]:
                combos_permutations_match.append(permutations_arr[j])

        df = pd.DataFrame(combos_permutations_match, columns=selected_features_x)
        df = df.to_numpy()

        for i in range(0, len(df)):
            if all_counter <= 113 and counter < 3:
                selections.append(df[i])
                all_counter+=1
                counter+=1
            elif all_counter >113 and counter < 2:
                selections.append(df[i])
                all_counter += 1
                counter += 1
            else:
                counter = 0
                break

    pd.DataFrame(selections).to_csv(str(directory[:-4]+'.csv'), index=False)
    submissionarr = []
    players = pd.read_csv('C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/08252021LADSD_BEFORE_GAME_reduced_players_list.csv').to_numpy()
    for i in range(0,len(selections)):
        arr = []
        arr.append(players[int(selections[i][1])][0])
        arr.append(players[int(selections[i][2])][0])
        arr.append(players[int(selections[i][3])][0])
        arr.append(players[int(selections[i][4])][0])
        arr.append(players[int(selections[i][5])][0])
        submissionarr.append(arr)
    pd.DataFrame(submissionarr).to_csv(str(directory[:-10] + 'submissions.csv'), index=False)



def MLTIME():

    table = pd.read_csv('C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALLMVPSTARPERMUTATIONS.csv')
    selected_features = ['Salary','Player1Rank','Player2Rank','Player3Rank','Player4Rank','Player5Rank','LineupMeanRank','Player1BattingOrder','Player2BattingOrder','Player3BattingOrder','Player4BattingOrder','Player5BattingOrder','LineupMeanBattingOrder','Predicted DFS Score Percentile Rank','Actual DFS Score Percentile Rank']
    table = table[selected_features]

    selected_features_x = ['Salary','Player1Rank','Player2Rank','Player3Rank','Player4Rank','Player5Rank','LineupMeanRank','Player1BattingOrder','Player2BattingOrder','Player3BattingOrder','Player4BattingOrder','Player5BattingOrder','LineupMeanBattingOrder','Predicted DFS Score Percentile Rank']
    selected_features_y = ['Actual DFS Score Percentile Rank']
    x = table[selected_features_x]
    y = table[selected_features_y]
    # print(x.shape)
    # print(y.shape)

    scaler = MinMaxScaler()
    x_scaled = scaler.fit_transform(x)
    y = y.values.reshape(-1, 1)
    y_scaled = scaler.fit_transform(y)
    # print(x_scaled.shape)
    # print(y_scaled.shape)

    x_train, x_test, y_train, y_test = train_test_split(x_scaled, y_scaled, test_size=0.25)
    # print(x_train.shape)
    # print(x_test.shape)
    # print(x_train, y_train)

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(units=100, activation='relu', input_shape=(14,)))
    model.add(tf.keras.layers.Dense(units=100, activation='relu'))
    model.add(tf.keras.layers.Dense(units=100, activation='relu'))
    model.add(tf.keras.layers.Dense(units=1, activation='linear'))

    model.compile(optimizer='Adam', loss='mean_squared_error')
    epochs_hist = model.fit(x_train, y_train, epochs=100, batch_size=75, validation_split=0.2) #200, 75, .919 R2
    model.save('saved_model/')

    epochs_hist.history.keys()
    plt.plot(epochs_hist.history['loss'])
    plt.plot(epochs_hist.history['val_loss'])
    plt.title('Epochs vs. Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Training and Validation Loss')
    plt.show()

    y_predict = model.predict(x_test)
    plt.plot(y_test, y_predict, '^', color='r')
    plt.title("Y Predict From X")
    plt.xlabel("Model Predictions")
    plt.ylabel("True Values")
    plt.show()

    y_predict_original = scaler.inverse_transform(y_predict)
    y_test_original = scaler.inverse_transform(y_test)
    plt.plot(y_test_original, y_predict_original, '^', color='r')
    plt.title("Y Predict From X")
    plt.xlabel("Model Predictions")
    plt.ylabel("True Values")

    k = x_test.shape[1]
    n = len(x_test)
    RMSE = np.sqrt(mean_squared_error(y_test_original, y_predict_original))
    MSE = mean_squared_error(y_test_original, y_predict_original)
    MAE = mean_absolute_error(y_test_original, y_predict_original)
    r2 = r2_score(y_test_original, y_predict_original)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
    print('RMSE =', RMSE, '\nMSE =', MSE, '\nMAE =', MAE, '\nR2 =', r2, '\nAdjusted R2 =', adj_r2)

def ML2(directory):
    table = pd.read_csv(directory)

    selected_features_x = ['Salary', 'Player1Rank', 'Player2Rank', 'Player3Rank', 'Player4Rank', 'Player5Rank',
                           'LineupMeanRank', 'Player1BattingOrder', 'Player2BattingOrder', 'Player3BattingOrder',
                           'Player4BattingOrder', 'Player5BattingOrder', 'LineupMeanBattingOrder',
                           'Predicted DFS Score Percentile Rank']
    table = table[selected_features_x]

    model = tf.keras.models.load_model('saved_model/')
    prediction = model.predict(table)

    l = []
    for i in prediction:
        l.append(i[0])

    table = pd.read_csv(directory)

    table['Prediction'] = l
    table['Prediction'] = table.Prediction.rank(pct=True)
    col = []
    for i in table:
        col.append(i)
    newarray = table.to_numpy()
    newarray = sorted(newarray, key=lambda x: x[-1], reverse=True)
    pd.DataFrame(newarray).to_csv('C:/Users/samue/PycharmProjects/MLBFanduelProject/FANDUEL/SingleGameDFS/ContestsOutput/ALL/test/killme.csv', index=False, header=col)
    return newarray







main()