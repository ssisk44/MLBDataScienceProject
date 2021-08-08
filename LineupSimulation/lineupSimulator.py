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
    PAOutcome(1,0)
    # simulate_games(1)


def PAOutcome(team, batter):
    num = random.randint(0, 10001) / 10000
    df = []
    if team == 1 or team == 2:               # FIX FOR HOME AND AWAY TEAMS CSVS
        df = pd.read_csv('dummyBattingLineup.csv').to_numpy()
    PA = df[batter][1]
    WalkGroup = df[batter][11] + df[batter][20]
    # SacGroup = df[batter][21] + df[batter][22]
    # KGroup = df[batter][12]
    # ErrorGroup = df[batter][24]
    HitGroup = df[batter][4]

    # OTHER LINEUP MATH FUNCTIONS
    # AVG = HitGroup / (PA - WalkGroup - SacGroup)
    #
    Singles = df[batter][4] - (df[batter][5] + df[batter][6] + df[batter][7])
    Doubles = df[batter][5]
    Triples = df[batter][6]
    HRs = df[batter][7]
    bases = Singles + (2*Doubles) + (3*Triples) + (4*HRs)
    # battingouts = PA - WalkGroup - HitGroup

    hitavgPA = HitGroup/PA
    outavgPA = (PA - WalkGroup - HitGroup)/PA
    walkavgPA = WalkGroup/PA
    #print(str(hitavgPA+outavgPA+walkavgPA)) SHOULD ALWAYS BE 1 BECAUSE SUM OF OUTCOMES
    #print(num, Singles/PA, (Singles+Doubles)/PA, (Singles+Doubles+Triples)/PA, (Singles+Doubles+Triples+HRs)/PA, hitavgPA+outavgPA) SHOWS OUTCOME FOR H(type) W O
    if num <= hitavgPA:
        if num <= Singles/PA:
            print("1B")
        elif Singles/PA < num <= (Singles+Doubles)/PA:
            print("2B")
        elif (Singles+Doubles)/PA < num <= (Singles+Doubles+Triples)/PA:
            print("3B")
        elif (Singles+Doubles+Triples)/PA < num <= (Singles+Doubles+Triples+HRs)/PA:
            print("HR")

    elif hitavgPA < num <= hitavgPA+outavgPA:
        print("O")
        return "Out"

    else:
        print("W")
        return "Walk"




def simulate_games(number_of_games):
    for games in range(0, number_of_games):
        # SCORE
        away_score = 0
        home_score = 0

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

                elif half_inning_counter % 2 == 1:
                    #away team hitting
                    PAOutcome(1, away_lineup_index)

                elif half_inning_counter % 2 == 0:
                    #home team hitting
                    PAOutcome(0, home_lineup_index)


                print('Game: ' + str(games+1) + ' Inning: ', inning_counter, ' Half Inning:', half_inning_counter, ' Outs:', outs_counter) # PRINTS OUT GAME INNINGS AND OUTS AS CHECK
                outs_counter += 1  # half inning logic
            outs_counter = 0  # inning logic

        print("Game #" + str(games+1) + " over --- Home:" + str(home_score) + " Away:" + str(away_score)) #PRINTS RESULT OF GAME


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
