import pandas as pd
import numpy as np
import math, random, time

########################################################################################################################
# GOAL: Create a logical baseball simulation for all possible batting outcomes that can predict base lineup output for a
# dummy/control lineup of all the same stats for thousands of games ---- AKA testing for lineup position bias
########################################################################################################################

### QUESTIONS ###
# How does the NL batting the pitcher at 9 effect the hitters nearest and their statistics potential

#Control Player: Trea Turner 08/03/2021

def main():
    average = 0
    for i in range(0,100000):
        result = determinePlateAttemptOutcome()
        average += result
    print(average/100000)


def determinePlateAttemptOutcome():
    num = random.randint(1, 10000)/10000
    if num <= 0.322:
        print('wee')


main()