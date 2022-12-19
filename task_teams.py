import json
import requests
from datetime import datetime
import re
import pandas as pd

'''
Returns a list of active team ids.
'''
def get_team_ids():
    teams_data = json.loads(requests.get('https://statsapi.web.nhl.com/api/v1/teams').text)
    ids = []
    for team in teams_data['teams']:
        ids.append(team['id'])
    return ids

'''
Calls the nhl team api and returns a JSON of basic team data.
'''
def get_team_data():
    request_string = 'https://statsapi.web.nhl.com/api/v1/teams/?expand=team.stats'
    team_data_json = json.loads(requests.get(request_string).text)
    team_data_all = []
    for team in team_data_json['teams']:
        team_data = {}
        team_data['id'] = team['id']
        team_data['teamname'] = team['teamName']
        team_data['name'] = team['name']
        team_data['division'] = team['division']['name']
        team_data['divisionshort'] = team['division']['nameShort']
        team_data['abbreviation'] = team['abbreviation']
        team_data['lastupdated'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

        stats_all = team['teamStats'][0]['splits']

        for k, v in stats_all[0]['stat'].items():
            team_data[k.lower()] = v
        
        for k, v in stats_all[1]['stat'].items():
            team_data[k.lower() + '_r'] = int(re.sub('\D', '', v))

        team_data['pytha_exp'] = pytha_exp(team_data['goalsagainstpergame'], team_data['goalspergame'], team_data['gamesplayed'])
        team_data['win_perc'] = round((team_data['wins']/team_data['gamesplayed']), 3)
        team_data['win_pytha_diff'] = round((team_data['pytha_exp']- team_data['win_perc']) , 3)
        team_data_all.append(team_data)
    return(team_data_all)

'''
Writes the teams data to a csv. This file will be used by the front end to develop views.
'''
def write_team_data():
    df = pd.DataFrame(get_team_data())
    df.to_csv('static/data/data_teams.csv', encoding='utf-8', index=False)

'''
Pythagorean expectation is a sports analytics formula devised by Bill James to estimate the percentage of games a baseball team "should" have won based on the number of runs they scored and allowed. Comparing a team's actual and Pythagorean winning percentage can be used to make predictions and evaluate which teams are over-performing and under-performing.

The exponent for baseball is close but not the best fit for hockey. The Dayaratna and Miller study verified the statistical legitimacy of making these assumptions and estimated the Pythagorean exponent for ice hockey to be slightly above 2.
'''
def pytha_exp(goals_allowed_per_game, goals_scored_per_game, total_games_played):
    EXPO = 2.1
    goals_allowed = goals_allowed_per_game * total_games_played
    goals_scored = goals_scored_per_game * total_games_played

    return(
       round(
         (goals_scored ** EXPO) / ((goals_scored ** EXPO) + (goals_allowed ** EXPO)) , 3
       )
    )
