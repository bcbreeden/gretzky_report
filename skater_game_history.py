import pandas as pd
from script_utils import get_data_path

def read_skater_history_data():
    return(pd.read_csv(get_data_path('data_game_history_skater.csv'), float_precision='round_trip'))

def get_skater_history_by_id(player_id):
    DATA  = read_skater_history_data()
    skater_history = DATA.loc[DATA['player_id']==int(player_id)]
    return(skater_history)