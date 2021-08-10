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
    simulate_games(1)


def simulate_games(number_of_games):
    for games in range(0, number_of_games):
        # SCORE
        away_score = 0
        home_score = 0

        ### BASIC OFFENSE VARIABLES
        away_lineup_index = 0
        home_lineup_index = 0

        baserunners_index = [-1, -1, -1]  # baserunners index with player index number or -1 if none

        inning_counter = 1
        half_inning_counter = 1  # 0 is None, odd is Top, even is Bottom, 1-18 for a normal game

        game_over = False
        while not game_over:  ### GAME
            if half_inning_counter >= 18 and away_score != home_score and half_inning_counter % 2 == 0:
                game_over = True
                break

            outs_counter = 0
            half_inning_over = False
            while not half_inning_over:  ### HALF INNING

                def PAOutcomeBasic(team, batter):
                    num = random.randint(0, 10001) / 10000
                    df_IN = []
                    if team == 1 or team == 2:  ### FIX FOR HOME AND AWAY TEAMS CSVS
                        df_IN = pd.read_csv('batting_stats_IN.csv').to_numpy()

                    PA = df_IN[batter][1]
                    WalkGroup = df_IN[batter][11] + df_IN[batter][20]
                    # SacGroup = df[batter][21] + df[batter][22]
                    # KGroup = df[batter][12]
                    # ErrorGroup = df[batter][24]
                    HitGroup = df_IN[batter][4]
                    ### OTHER LINEUP MATH FUNCTIONS
                    # AVG = HitGroup / (PA - WalkGroup - SacGroup)
                    Singles = df_IN[batter][4] - (df_IN[batter][5] + df_IN[batter][6] + df_IN[batter][7])
                    Doubles = df_IN[batter][5]
                    Triples = df_IN[batter][6]
                    HRs = df_IN[batter][7]
                    # bases = Singles + (2 * Doubles) + (3 * Triples) + (4 * HRs)
                    # battingouts = PA - WalkGroup - HitGroup
                    hitavgPA = HitGroup / PA
                    outavgPA = (PA - WalkGroup - HitGroup) / PA
                    walkavgPA = WalkGroup / PA
                    # print(str(hitavgPA+outavgPA+walkavgPA)) SHOULD ALWAYS BE 1 BECAUSE SUM OF OUTCOMES
                    # print(num, Singles/PA, (Singles+Doubles)/PA, (Singles+Doubles+Triples)/PA, (Singles+Doubles+Triples+HRs)/PA, hitavgPA+outavgPA) SHOWS OUTCOME FOR H(type) W O

                    df_OUT = pd.read_csv('batting_stats_OUT.csv').to_numpy()
                    df_OUT[batter][1] = int(df_OUT[batter][1]) + 1  # PA
                    ###### for each outcome 1)record to csv  2)alter game conditions ex. score, baserunners ######
                    if num <= hitavgPA:
                        df_OUT[batter][4] = int(df_OUT[batter][4]) + 1  # H
                        df_OUT[batter][2] = int(df_OUT[batter][2]) + 1  # AB
                        if num <= Singles / PA:
                            return "1B"

                        elif Singles / PA < num <= (Singles + Doubles) / PA:
                            df_OUT[batter][5] = int(df_OUT[batter][5]) + 1  # 2b
                            return "2B"

                        elif (Singles + Doubles) / PA < num <= (Singles + Doubles + Triples) / PA:
                            df_OUT[batter][6] = int(df_OUT[batter][6]) + 1  # 3b
                            return "3B"

                        elif (Singles + Doubles + Triples) / PA < num <= (Singles + Doubles + Triples + HRs) / PA:
                            df_OUT[batter][7] = int(df_OUT[batter][7]) + 1  # HR
                            return "HR"

                    elif hitavgPA < num <= hitavgPA + outavgPA:
                        df_OUT[batter][2] = int(df_OUT[batter][2]) + 1  # AB
                        return "O"

                    else:
                        df_OUT[batter][11] = int(df_OUT[batter][11]) + 1  # BB
                        return "BB"

                    df_OUT.to_csv("batting_stats_OUT", index=False)

                if half_inning_counter % 2 == 1:
                    ### away team hitting
                    outcome = PAOutcomeBasic(1, away_lineup_index)  # plate outcome
                    BaseRunningEventAdvancement(1, away_lineup_index, baserunners_index, outcome)

                    checklineupreset(away_lineup_index)  # increment lineup index

                elif half_inning_counter % 2 == 0:
                    ### home team hitting
                    outcome = PAOutcomeBasic(0, home_lineup_index)
                    if outcome == "O":
                        outs_counter += 1
                    else:
                        BaseRunningEventAdvancement(0, away_lineup_index, baserunners_index, outcome)

                    checklineupreset(home_lineup_index)

                if outs_counter >= 3:  # half inning logic
                    if half_inning_counter % 2 == 0:
                        half_inning_counter += 1
                        inning_counter += 1
                        break
                    else:
                        half_inning_counter += 1
                        break
                # print('Game: ' + str(games+1) + ' Inning: ', inning_counter, ' Half Inning:', half_inning_counter, ' Outs:', outs_counter) # PRINTS OUT GAME INNINGS AND OUTS AS CHECK

                outs_counter += 1  # half inning logic

            ### inning logic to reset outs and baserunners
            outs_counter, runner_on_first_index, runner_on_second_index, runner_on_third_index = 0, None, None, None

        print("Game #" + str(games + 1) + " over --- Home:" + str(home_score) + " Away:" + str(
            away_score))  # PRINTS RESULT OF GAME

        #### resets game score for next game
        home_score, away_score = 0, 0


# def BaseRunningEventPrePitch(team, playerindex):
#     print("")


def BaseRunningEventAdvancement(team, batterindex, baserunners, hittype):
    if hittype == "1B" or hittype == "BB":
        "advance"

    # return (baserunners,runs scored)


def checklineupreset(index):
    if index < 8:
        index += 1
        return index
    else:
        return 0


main()
