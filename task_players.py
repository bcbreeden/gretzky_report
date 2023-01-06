import json
import requests
from task_teams import get_team_ids
from script_utils import get_min_games
from datetime import datetime
import pandas as pd
from script_utils import get_data_path, get_current_season

'''
Calls the nhl team api and returns a list of all active player ids.
'''
def get_player_ids():
    player_ids = []

    for team_id in get_team_ids():
        request_string = 'https://statsapi.web.nhl.com/api/v1/teams/{}/roster'.format(team_id)
        team_roster_data = json.loads(requests.get(request_string).text)

        for player in team_roster_data['roster']:
            player_ids.append(player['person']['id'])
        
    return(player_ids)

'''
Makes a request for each player and records the player statistics.

Returns two lists of player records: [player_stats_skaters, player_stats_goalies]
'''
def get_player_stats():
    player_stats_skaters = []
    player_stats_goalies = []

    for player_id in get_player_ids():
        request_string = 'https://statsapi.web.nhl.com/api/v1/people/{}?hydrate=stats(splits=statsSingleSeason)'.format(player_id)
        player_data = json.loads(requests.get(request_string).text)

        if (player_data['people'][0]['primaryPosition']['abbreviation'] == 'G'):
            record = {}

            # People Info
            log_string = 'Goalie Record Found: {} {}'.format(str(player_data['people'][0]['id']), player_data['people'][0]['fullName'])
            print(log_string, flush=True)

            record['id'] = player_data['people'][0]['id']
            record['currentteamid'] = player_data['people'][0]['currentTeam']['id']
            record['fullname'] = player_data['people'][0]['fullName']
            record['currentteam'] = player_data['people'][0]['currentTeam']['name']
            # record['primaryposition'] = player_data['people'][0]['primaryPosition']['name']
            

            # Stats Info
            # Check for stats
            try:
                stats = player_data['people'][0]['stats'][0]['splits'][0]['stat']
                record['wins'] = stats['wins']
                record['losses'] = stats['losses']
                record['ties'] = stats['ties']
                record['shutouts'] = stats['shutouts']
                record['savepercentage'] = stats['savePercentage']
                record['goalagainstaverage'] = stats['goalAgainstAverage']
            # No Stats (Rookie or First NHL Game)
            except (IndexError, KeyError):
                record['wins'] = 0
                record['losses'] = 0
                record['ties'] = 0
                record['shutouts'] = 0
                record['savepercentage'] = 0
                record['goalagainstaverage'] = 0
            # record['lastupdated'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            player_stats_goalies.append(record)
            

        else:
            record = {}

            # People Info
            log_string = 'Skater Record Found: {} {}'.format(str(player_data['people'][0]['id']), player_data['people'][0]['fullName'])
            print(log_string, flush=True)

            record['id'] = player_data['people'][0]['id']
            record['teamid'] = player_data['people'][0]['currentTeam']['id']
            record['playername'] = player_data['people'][0]['fullName']
            record['currentteam'] = player_data['people'][0]['currentTeam']['name']
            record['position'] = player_data['people'][0]['primaryPosition']['name']

            # Stats Info
            # Check for stats
            try:
                stats = player_data['people'][0]['stats'][0]['splits'][0]['stat']
                record['goals'] = stats['goals']
                record['GPG'] = round(stats['goals']/stats['games'], 2)
                record['assists'] = stats['assists']
                record['APG'] = round(stats['assists']/stats['games'], 2)
                # record['pim'] = stats['pim']
                record['shots'] = stats['shots']
                record['SPG'] = round(stats['shots']/stats['games'], 2)
                record['games'] = stats['games']
                # record['hits'] = stats['hits']
                # record['powerplaygoals'] = stats['powerPlayGoals']
                # record['powerplaypoints'] = stats['powerPlayPoints']
                # record['faceoffpct'] = stats['faceOffPct']
                # record['plusminus'] = stats['plusMinus']
                record['points'] = stats['points']
                record['PPG'] = round(stats['points']/stats['games'], 2)
                record['blocked'] = stats['blocked']
                record['BPG'] = round(stats['blocked']/stats['games'], 2)
                record['timeonicepergame'] = float(stats['timeOnIcePerGame'].replace(":", "." ))

            # No Stats (First NHL Game)
            except (IndexError, KeyError):
                record['goals'] = 0
                record['GPG'] = 0
                record['assists'] = 0
                record['APG'] = 0
                # record['pim'] = 0
                record['shots'] = 0
                record['SPG'] = 0
                record['games'] = 0
                # record['hits'] = 0
                # record['powerplaygoals'] = 0
                # record['powerplaypoints'] = 0
                # record['faceoffpct'] = 0
                # record['plusminus'] = 0
                record['points'] = 0
                record['PPG'] = 0
                record['blocked'] = 0
                record['BPG'] = 0
                record['timeonicepergame'] = 0
            # record['lastupdated'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

            if record['games'] >= get_min_games():
                print('Player added:', player_data['people'][0]['fullName'], flush=True)
                player_stats_skaters.append(record)
            else:
                print('Not enough games for:', player_data['people'][0]['fullName'], flush=True)
    return(player_stats_skaters, player_stats_goalies)

'''
Takes in player data and writes the data to a csv file. One for skater and another for goalies (they have different features which dictates we need two seperate files.)
'''
def write_player_data():
    data_all = get_player_stats()
    skater_df = pd.DataFrame(data_all[0])
    goalie_df = pd.DataFrame(data_all[1])
    skater_df.to_csv(get_data_path('data_skater.csv'), encoding='utf-8', index=False)
    goalie_df.to_csv(get_data_path('data_goalie.csv'), encoding='utf-8', index=False)

def get_player_game_history():
    GAMES_NEEDED = 5
    player_ids = get_player_ids()
    # player_ids = [8477970]

    player_game_history_skaters = []
    player_game_history_goalies = []
    for player_id in player_ids:
        print('Player ID:', player_id, flush=True)
        request_string = 'https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=gameLog&season={}'.format(player_id, get_current_season())
        player_game_history_data = json.loads(requests.get(request_string).text)
        games = player_game_history_data['stats'][0]['splits']
        for game in games[:GAMES_NEEDED]:
            record= {}
            record['player_id'] = player_id
            record['date'] = game['date']
            record['opp_id'] = game['opponent']['id']
            record['home_game'] = game['isHome']
            record['TOI'] = game['stat']['timeOnIce']
            try:
                record['assists'] = game['stat']['assists']
                record['goals'] = game['stat']['goals']
                record['shots'] = game['stat']['shots']
                record['PPTOI'] = game['stat']['powerPlayTimeOnIce']
                record['blocked'] = game['stat']['blocked']
                player_game_history_skaters.append(record)
                print('Skater record add for {} {}.'.format(player_id, record['date']), flush=True)
            except KeyError:
                try:
                    record['saves'] = game['stat']['saves']
                    record['save_perc'] = game['stat']['savePercentage']
                    record['goals_against'] = game['stat']['goalsAgainst']
                    record['shots_against'] = game['stat']['shotsAgainst']
                    player_game_history_goalies.append(record)
                    print('Goalie record add for {}.'.format(player_id), flush=True)
                except Exception:
                    print('Data not found or data corrupt for this game. Skipping record', flush=True)

    return(player_game_history_skaters, player_game_history_goalies)

def write_player_game_history_data():
    data_all = get_player_game_history()
    skater_df = pd.DataFrame(data_all[0])
    goalie_df = pd.DataFrame(data_all[1])
    skater_df.to_csv(get_data_path('data_game_history_skater.csv'), encoding='utf-8', index=False)
    print('Skater game history file written successfully!', flush=True)
    goalie_df.to_csv(get_data_path('data_game_history_goalie.csv'), encoding='utf-8', index=False)
    print('Goalie game history file written successfully!', flush=True)
