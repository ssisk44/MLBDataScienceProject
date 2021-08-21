import pandas as pd

file = 'SingleGameContestCSVs/08182021PITLAD'

index = 5
array = pd.read_csv("C:/Users/samue/PycharmProjects/MLBFanduelProject/ALL_DATA/DailyBoxScores/" + file[21:30] + "_all_box_scores.csv").to_numpy()
print(index)
newarr = eval(array[index][3])
print(newarr)