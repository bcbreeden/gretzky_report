import pandas as pd
from datetime import date, datetime

DATA = pd.read_csv('static/data/data_schedule.csv', float_precision='round_trip')
# DATA = pd.read_csv('/home/breedenb/pyhl-io/static/data/data_schedule.csv', float_precision='round_trip')

'''
Returns the ids of all teams playing today.
'''
def get_teams_playing_today():
    today = date.today().strftime('%Y-%m-%d')
    schedule_today = DATA.loc[DATA['gamedate']==today]
    ids = []
    for _, game in schedule_today.iterrows():
        ids.append(game['homeid'])
        ids.append(game['awayid'])
    return(ids)