import pandas as pd
from script_utils import get_data_path

DATA = pd.read_csv(get_data_path('data_teams.csv'), float_precision='round_trip')

'''
Fetches team data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_team_data_by_id(team_id):
    team = DATA.loc[DATA['id']==int(team_id)]
    # teams = DATA.loc[DATA['column_name'].isin(team_id)]
    return(team)

'''
Fetches team data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_team_data_all():
    # teams = DATA
    teams = DATA.sort_values(by=['name'])
    print(teams.head())
    return(teams)

'''
Locate and return data for multiple teams by a list of ids.
'''
def get_teams_data_by_team_ids(team_ids):
    teams = DATA.loc[DATA['id'].isin(team_ids)]
    return(teams)
