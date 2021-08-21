import math

import pybaseball
from numpy import arctan
from pybaseball import *
import tensorflow as tf
from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
from math import sqrt, pi

headers = ['pitch_type', 'game_date', 'release_speed', 'release_pos_x', 'release_pos_z', 'player_name', 'batter',
           'pitcher', 'events', 'description', 'spin_dir', 'spin_rate_deprecated', 'break_angle_deprecated',
           'break_length_deprecated', 'zone', 'des', 'game_type', 'stand', 'p_throws', 'home_team', 'away_team', 'type',
           'hit_location', 'bb_type', 'balls', 'strikes', 'game_year', 'pfx_x', 'pfx_z', 'plate_x', 'plate_z', 'on_3b',
           'on_2b', 'on_1b', 'outs_when_up', 'inning', 'inning_topbot', 'hc_x', 'hc_y', 'tfs_deprecated',
           'tfs_zulu_deprecated', 'fielder_2', 'umpire', 'sv_id', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'sz_top',
           'sz_bot', 'hit_distance_sc', 'launch_speed', 'launch_angle', 'effective_speed', 'release_spin_rate',
           'release_extension', 'game_pk', 'pitcher.1', 'fielder_2.1', 'fielder_3', 'fielder_4', 'fielder_5',
           'fielder_6', 'fielder_7', 'fielder_8', 'fielder_9', 'release_pos_y', 'estimated_ba_using_speedangle',
           'estimated_woba_using_speedangle', 'woba_value', 'woba_denom', 'babip_value', 'iso_value',
           'launch_speed_angle', 'at_bat_number', 'pitch_number', 'pitch_name', 'home_score', 'away_score', 'bat_score',
           'fld_score', 'post_away_score', 'post_home_score', 'post_bat_score', 'post_fld_score',
           'if_fielding_alignment', 'of_fielding_alignment', 'spin_axis', 'delta_home_win_exp', 'delta_run_exp']

def main():
    # getEveryMLBPitchStats()
    # parseBIPFromEveryMLBPitchStats()
    # LA_LS_Distance_ML()
    # plotBIP()
    # getPitcherStatcast('Kershaw', 'Clayton', 'LAD', '2021-08-01', '2021-08-18')
    getBatterStatcast('Alonso', 'Pete', 'NYM', '2021-08-01', '2021-08-18')
    # getBattingbySeason(2019,2019)
    # getStandings(2021)
    # getScheduleandResults(2021, 'NYY')


### GENERAL STATCAST DATA
def getEveryMLBPitchStats(start_date, end_date):
    stats = statcast(start_date, end_date)
    headers = []
    for col in stats:
        headers.append(col)
    stats.to_csv(r''+start_date+'_'+end_date+'_every_MLB_pitch_stats.csv', index=False, header=headers)

### BATTER STATCAST DATA
def getBatterStatcast(lname, fname, team, start_date, end_date):
    b_id = playerid_lookup(lname, fname)['key_mlbam'][0] # changes on number of players with same name
    statcast_batter(start_date, end_date, b_id).to_csv(fname+'_'+lname+"_Hitting.csv") # date formatted '2021-08-01'

def getBattingbySeason(start_season, end_season):
    batting_stats(start_season, end_season).to_csv(str(start_season+1)+'_to_'+str(end_season)+"_Hitting.csv")

def getBattingbyDateRange(start_date, end_date):
    batting_stats_range(start_date, end_date).to_csv(start_date+'_'+end_date+"_Hitting.csv") # date formatted '2021-08-01'

# def getBattingbySingleSeason(season): BIG TIME BUSTED
#     batting_stats_bref(season).to_csv(str(season)+"_Hitting.csv")


### PITCHING STATCAST DATA
def getPitcherStatcast(fname, lname, team, start_date, end_date):
    p_id = playerid_lookup('Kershaw', 'Clayton')['key_mlbam'][0] #changes on number of players with same name
    statcast_batter(start_date, end_date, p_id).to_csv(fname+'_'+lname+"_Pitching.csv") # date formatted '2021-08-01'

def getPitchingbySeason(start_season, end_season):
    pitching_stats(start_season, end_season).to_csv(str(start_season+1)+'_to_'+str(end_season)+"_Pitching.csv")

def getPitchingbyDateRange(start_date, end_date):
    pitching_stats_range(start_date, end_date).to_csv(start_date+'_'+end_date+"_Pitching.csv") # date formatted '2021-08-01'

# def getPitchingbySingleSeason(season): BIG TIME BUSTED
#     pitching_stats_bref(season).to_csv(str(season)+"_Pitching.csv")


### SCHEDULE AND RESULTS
def getScheduleandResults(year, teamabbrev):
    schedule_and_record(year, teamabbrev).to_csv(str(year) + '_' + teamabbrev + "_schedule_and_results.csv")  # date formatted '2021-08-01'

def getStandings(year):
    pd.DataFrame(standings(year)).to_csv(str(year) + "_standings.csv")  # date formatted '2021-08-01'


### OTHER
def parseBIPFromEveryMLBPitchStats():
    stats = pd.read_csv('batting.csv').to_numpy()
    hit_array = []
    for i in range(0, len(stats)):
        if str(stats[i][9]) == "hit_into_play":
            hit_array.append(stats[i])
    print("Array Length of all Pitches put in Play: " + str(len(hit_array)))
    pd.DataFrame(hit_array).to_csv(r'hits_off_BIP.csv', index=False, header=headers)

def threeDimensionalPlot():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.show()

def plotBIP():

    table = pd.read_csv('hits_off_pitchers.csv')
    selected_features = ['hc_x', 'hc_y', 'hit_distance_sc', 'launch_angle']
    table = table[selected_features]
    table['spray_angle'] = np.nan

    table = table[table['launch_angle'] >= 0]
    table = table[table['hit_distance_sc'] >= 0].to_numpy()

    for i in range(0, len(table)):
        if table[i][2] > 450:
            print(i, table[i][2])

    for i in range(0, len(table)):
        table[i][0] = table[i][0] - 130
        table[i][1] = 213 - table[i][1]
        table[i][4] = -arctan((table[i][0]) / (table[i][1]))

    for i in range(0, len(table)):
        print(table[i][4])
    headers = ['hc_x', 'hc_y', 'hit_distance_sc', 'launch_angle','spray_angle']
    table = pd.DataFrame(data = table, columns= headers)
    sns.scatterplot(table['hc_x'], table['hc_y'], table['launch_angle'], alpha=1).set(title="Hit X vs Hit Y")
    plt.show()








if __name__ == '__main__':
    main()