import pandas as pd
from script_utils import get_data_path

def read_teams_data():
    return(pd.read_csv(get_data_path('data_teams.csv'), float_precision='round_trip'))

'''
Fetches team data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_team_data_by_id(team_id):
    DATA = read_teams_data()
    team = DATA.loc[DATA['id']==int(team_id)]
    return(team)

'''
Fetches team data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_team_data_all():
    DATA = read_teams_data()
    teams = DATA.sort_values(by=['name'])
    return(teams)

'''
Locate and return data for multiple teams by a list of ids.
'''
def get_teams_data_by_team_ids(team_ids):
    DATA = read_teams_data() 
    #teams = DATA.loc[DATA['id'].isin(team_ids)] #ordered by team id
    teams = DATA.set_index('id').loc[team_ids].reset_index() #ordered by the values passed in
    return(teams)

def get_team_ids_all():
    DATA = read_teams_data()
    return(list(DATA.loc[:,"id"]))