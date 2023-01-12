import pandas as pd
from datetime import date, datetime
from script_utils import get_data_path

# DATA = pd.read_csv(get_data_path('data_schedule.csv'), float_precision='round_trip')

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