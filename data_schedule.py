import pandas as pd
from datetime import date, datetime
from script_utils import get_data_path

def read_schedule_data():
    return(pd.read_csv(get_data_path('data_schedule.csv'), float_precision='round_trip'))

'''
Returns the ids of all teams playing today.
'''
def get_teams_playing_today():
    DATA = read_schedule_data()

    today = date.today().strftime('%Y-%m-%d')
    schedule_today = DATA.loc[DATA['gamedate']==today]
    ids = []
    for _, game in schedule_today.iterrows():
        ids.append(game['homeid'])
        ids.append(game['awayid'])
    return(ids)

'''
Given a team id, returns the next team id they played against.
'''
def get_next_opponent(team_id):
    DATA = read_schedule_data()
    today = date.today().strftime('%Y-%m-%d')
    games_filtered = DATA[(DATA['gamedate'] >= today)]
    next_game = games_filtered[(games_filtered['homeid'] == team_id) | (DATA['awayid'] == team_id)].head(1)
    if next_game.iloc[0]['homeid'] == team_id:
        return next_game.iloc[0]['awayid']
    else:
        return next_game.iloc[0]['homeid']

'''
Given a team id, returns the last time id they played against.
'''
def get_last_opponent(team_id):
    DATA = read_schedule_data()
    today = date.today().strftime('%Y-%m-%d')
    games_filtered = DATA[(DATA['gamedate'] < today)]
    next_game = games_filtered[(games_filtered['homeid'] == team_id) | (DATA['awayid'] == team_id)].tail(1)
    if next_game.iloc[0]['homeid'] == team_id:
        return next_game.iloc[0]['awayid']
    else:
        return next_game.iloc[0]['homeid']
