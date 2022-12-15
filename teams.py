import pandas as pd

DATA = pd.read_csv('static/data/data_teams.csv')

'''
Fetches team data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_team_data_by_id(team_id):
    team = DATA.loc[DATA['id']==team_id]
    return(team)

'''
Fetches team data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_team_data_all():
    teams = DATA
    return(teams)
