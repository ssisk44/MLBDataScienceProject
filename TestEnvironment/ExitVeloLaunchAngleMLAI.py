import numpy as np
import pandas as pd
from keras.losses import mean_squared_error, mean_absolute_error
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from pybaseball import *


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
    getEveryMLBPitchStats()
    parseBIPFromEveryMLBPitchStats()
    LA_LS_Distance_ML()


def getEveryMLBPitchStats():
    stats = statcast('2021-08-15', '2021-08-17')
    headers = []
    for col in stats:
        headers.append(col)
    stats.to_csv(r'every_MLB_pitch_stats.csv', index=False, header=headers)

def parseBIPFromEveryMLBPitchStats():
    stats = pd.read_csv('batting.csv').to_numpy()
    hit_array = []
    for i in range(0, len(stats)):
        if str(stats[i][9]) == "hit_into_play":
            hit_array.append(stats[i])
    print("Array Length of all Pitches put in Play: " + str(len(hit_array)))
    pd.DataFrame(hit_array).to_csv(r'hits_off_BIP.csv', index=False, header=headers)

def LA_LS_Distance_ML():
    table = pd.read_csv('hits_off_pitchers.csv')
    selected_features = ['launch_speed', 'launch_angle', 'hit_distance_sc']
    table = table[selected_features]
    table = table[table['launch_angle'] >= 0]

    selected_features_x = ['launch_speed', 'launch_angle']
    selected_features_y = ['hit_distance_sc']
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
    model.add(tf.keras.layers.Dense(units=100, activation='relu', input_shape=(2,)))
    model.add(tf.keras.layers.Dense(units=100, activation='relu'))
    model.add(tf.keras.layers.Dense(units=100, activation='relu'))
    model.add(tf.keras.layers.Dense(units=1, activation='linear'))

    model.compile(optimizer='Adam', loss='mean_squared_error')
    epochs_hist = model.fit(x_train, y_train, epochs=10, batch_size=10, validation_split=0.2)

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
    RMSE = float(format(np.sqrt(mean_squared_error(y_test_original, y_predict_original)), '0.3f'))
    MSE = mean_squared_error(y_test_original, y_predict_original)
    MAE = mean_absolute_error(y_test_original, y_predict_original)
    r2 = r2_score(y_test_original, y_predict_original)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
    print('RMSE =', RMSE, '\nMSE =', MSE, '\nMAE =', MAE, '\nR2 =', r2, '\nAdjusted R2 =', adj_r2)


main()