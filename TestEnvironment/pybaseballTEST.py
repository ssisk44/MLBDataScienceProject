from pybaseball import *

#####https://github.com/jldbc/pybaseball/tree/master/docs#####

# pybaseball.batting()
data = statcast_batter('2008-04-01', '2008-07-15', player_id = 120074)

data.to_csv(r'batting.csv', index=False)
