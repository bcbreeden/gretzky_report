import pandas as pd
from script_utils import get_data_path
import matplotlib.pyplot as plt

def read_skater_history_data():
    return(pd.read_csv(get_data_path('data_game_history_skater.csv'), float_precision='round_trip'))

def get_skater_history_by_id(player_id):
    DATA  = read_skater_history_data()
    skater_history = DATA.loc[DATA['player_id']==int(player_id)]
    return(skater_history)

def get_skater_plot_data(skater_data):
    game_opponent_list = skater_data['opp'].tolist()
    game_fp_list = skater_data['fantasy_points'].tolist()
    return(game_opponent_list, game_fp_list)

