import pandas as pd
from script_utils import get_data_path
import matplotlib.pyplot as plt

def read_skater_history_data():
    return(pd.read_csv(get_data_path('data_game_history_skater.csv'), float_precision='round_trip'))

def get_skater_history_by_id(player_id):
    DATA  = read_skater_history_data()
    skater_history = DATA.loc[DATA['player_id']==int(player_id)]
    return(skater_history)

def get_skater_history_graph():
	#TODO add the data arguement to the function
    skater_history_df = get_skater_history_by_id(8474090) #dummy data
    print(skater_history_df)
    game_opponent = skater_history_df['opp'].tolist()
    game_fantasy_points = skater_history_df['fantasy_points'].tolist()
    plt.xlabel('Opponent')
    plt.ylabel('Fantasy Points')
    plt.plot(game_opponent, game_fantasy_points, '--o')
    plt.show()
