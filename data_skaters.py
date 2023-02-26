import pandas as pd
from script_utils import get_min_games, get_data_path, get_hot_cold_dif

def read_skater_data():
    return(pd.read_csv(get_data_path('data_skater.csv'), float_precision='round_trip'))

'''
Fetches skater data from the CSV file via a skater id.
'''
def get_skater_data_by_id(player_id):
    DATA  = read_skater_data()
    skater = DATA.loc[DATA['id']==int(player_id)]
    return(skater)

'''
Fetches skater data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_skaters_data_by_team_id(team_ids):
    DATA  = read_skater_data()
    skaters = DATA.loc[DATA['teamid'].isin(team_ids)]
    return(skaters)

def get_top_skaters(number, feature):
    DATA  = read_skater_data()
    skaters = DATA.sort_values(by=[feature])
    return(skaters)
   
def set_hot_cold():
    skater_data_all = read_skater_data()
    skater_game_history = pd.read_csv(get_data_path('data_game_history_skater.csv'), float_precision='round_trip')
    for index, skater in skater_data_all.iterrows():
        game_history = skater_game_history.loc[skater_game_history['player_id'] == skater['id']]
        fantasy_avg_5_games = game_history['fantasy_points'].mean()
        difference = (fantasy_avg_5_games - skater['FPPG'])
        if difference >= get_hot_cold_dif():
            skater_data_all.at[index,'hot'] = 1
        elif difference <= (get_hot_cold_dif() - (get_hot_cold_dif() * 2)):
            skater_data_all.at[index,'cold'] = 1
    skater_data_all.to_csv(get_data_path('data_skater.csv'), encoding='utf-8', index=False)
