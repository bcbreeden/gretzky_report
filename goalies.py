import pandas as pd
from script_utils import get_min_games, get_data_path, get_hot_cold_dif

def read_goalie_data():
    return(pd.read_csv(get_data_path('data_goalie.csv'), float_precision='round_trip'))

def get_goalies_data_by_team_id(team_ids):
    DATA  = read_goalie_data()
    goalies = DATA.loc[DATA['currentteamid'].isin(team_ids)]
    return(goalies)