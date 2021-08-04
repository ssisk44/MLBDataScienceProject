import pandas as pd
import numpy as np
import math, random, time


########################################################################################################################
# GOAL: Create a logical baseball simulation for all possible batting outcomes that can predict base lineup output for a
# dummy/control lineup of all the same stats for thousands of games ---- AKA testing for lineup position bias
########################################################################################################################

### QUESTIONS ###
# How does the NL batting the pitcher at 9 effect the hitters nearest and their statistics potential

# Control Player: Trea Turner 08/03/2021

def main():
    df = pd.read_csv('dummyBaserunningLineup.csv').to_numpy()
    simulate_games(1)


def PAOutcome(team, batter):
    num = random.randint(1, 10000) / 10000


def simulate_games(number_of_games):
    for games in range(0, number_of_games):
        # SCORE
        away_score = 0
        home_score = 1

        # BASIC OFFENSE VARIABLES
        away_lineup_index = 0
        home_lineup_index = 0
        runner_on_first_index = None
        runner_on_second_index = None
        runner_on_third_index = None

        inning_counter = 1
        half_inning_counter = 1  # 0 is None, odd is Top, even is Bottom, 1-18 for a normal game

        game_over = False
        while not game_over:  # GAME
            if half_inning_counter >= 18 and away_score != home_score and half_inning_counter % 2 == 0:
                game_over = True
                break

            outs_counter = 0
            half_inning_over = False
            while not half_inning_over:  # HALF INNING

                if outs_counter >= 3:  # half inning logic
                    if half_inning_counter % 2 == 0:
                        half_inning_counter += 1
                        inning_counter += 1
                        break
                    else:
                        half_inning_counter += 1
                        break

                # print('Inning: ', inning_counter, ' Half Inning:', half_inning_counter, ' Outs:', outs_counter) PRINTS OUT GAME INNINGS AND OUTS AS CHECK
                outs_counter += 1  # half inning logic
            outs_counter = 0  # inning logic

        # print("Gameover - Home:" + str(home_score) + " Away:" + str(away_score)) PRINTS RESULT OF GAME


def getBatterStats(team, playerindex):
    print("")

def getRunnerStats(team, playerindex):
    print("")

def checkBasesForRunners(team, first, second, third):
    print("")

def BaseRunningEventPrePitch(team, playerindex):
    print("")

def BattingEvent(team, playerindex):
    print("")

def BaseRunningEventAdvancement(team, playerindex):
    print("")




main()
