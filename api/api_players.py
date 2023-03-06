import json
import requests
from api.api_teams import get_team_ids
from datetime import datetime

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
def get_player_stats(min_games):
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
            record['teamid'] = player_data['people'][0]['currentTeam']['id']
            record['playername'] = player_data['people'][0]['fullName']
            record['currentteam'] = player_data['people'][0]['currentTeam']['name']
            record['status'] = player_data['people'][0]['rosterStatus']
            record['position'] = 'Goalie'
            # record['primaryposition'] = player_data['people'][0]['primaryPosition']['name']
            

            # Stats Info
            # Check for stats
            try:
                stats = player_data['people'][0]['stats'][0]['splits'][0]['stat']
                record['jerseynumber'] = player_data['people'][0]['primaryNumber']
                record['games'] = stats['games']
                record['wins'] = stats['wins']
                record['losses'] = stats['losses']
                record['ties'] = stats['ties']
                record['shutouts'] = stats['shutouts']
                record['savepercentage'] = stats['savePercentage']
                record['goalagainstaverage'] = stats['goalAgainstAverage']
                record['saves'] = stats['saves']
                record['ot'] = stats['ot']
                record['gamesstarted'] = stats['gamesStarted']
                record['FPPG'] = get_goalie_fantasy_ppg(record['games'], record['wins'], record['saves'], record['goalagainstaverage'], record['shutouts'], record['ot'])
            # No Stats (Rookie or First NHL Game)
            except (IndexError, KeyError):
                record['jerseynumber'] = 0
                record['games'] = 0
                record['wins'] = 0
                record['losses'] = 0
                record['ties'] = 0
                record['shutouts'] = 0
                record['savepercentage'] = 0
                record['goalagainstaverage'] = 0
                record['saves'] = 0
                record['ot'] = 0
                record['gamesstarted'] = 0
                record['FPPG'] = 0 
            record['hot'] = 0
            record['cold'] = 0
            record['lastupdated'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
            if record['games'] >= min_games:
                print('Player added:', player_data['people'][0]['fullName'], flush=True)
                player_stats_goalies.append(record)
            else:
                print('Not enough games for:', player_data['people'][0]['fullName'], flush=True)
            

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
            record['status'] = player_data['people'][0]['rosterStatus']

            # Stats Info
            # Check for stats
            try:
                stats = player_data['people'][0]['stats'][0]['splits'][0]['stat']
                record['jerseynumber'] = player_data['people'][0]['primaryNumber']
                record['goals'] = stats['goals']
                record['GPG'] = round(stats['goals']/stats['games'], 2)
                record['assists'] = stats['assists']
                record['APG'] = round(stats['assists']/stats['games'], 2)
                record['pim'] = stats['pim']
                record['shots'] = stats['shots']
                record['SPG'] = round(stats['shots']/stats['games'], 2)
                record['games'] = stats['games']
                record['hits'] = stats['hits']
                record['powerplaygoals'] = stats['powerPlayGoals']
                record['powerplaypoints'] = stats['powerPlayPoints']
                record['faceoffpct'] = stats['faceOffPct']
                record['plusminus'] = stats['plusMinus']
                record['blocked'] = stats['blocked']
                record['BPG'] = round(stats['blocked']/stats['games'], 2)
                record['points'] = stats['points']
                record['PPG'] = round(stats['points']/stats['games'], 2)
                record['FPPG'] = round(get_skater_fantasy_ppg(
                    record['GPG'],
                    record['APG'],
                    record['SPG'],
                    record['BPG']
                ), 2)
                record['timeonicepergame'] = float(stats['timeOnIcePerGame'].replace(":", "." ))
                record['powerPlayTimeOnIcePerGame'] = float(stats['powerPlayTimeOnIcePerGame'].replace(":", "." ))

            # No Stats (First NHL Game)
            except (IndexError, KeyError):
                record['jerseynumber'] = 0
                record['goals'] = 0
                record['GPG'] = 0
                record['assists'] = 0
                record['APG'] = 0
                record['pim'] = 0
                record['shots'] = 0
                record['SPG'] = 0
                record['games'] = 0
                record['hits'] = 0
                record['powerplaygoals'] = 0
                record['powerplaypoints'] = 0
                record['faceoffpct'] = 0
                record['plusminus'] = 0
                record['blocked'] = 0
                record['BPG'] = 0
                record['points'] = 0
                record['PPG'] = 0
                record['FPPG'] = 0
                record['timeonicepergame'] = 0
                record['powerPlayTimeOnIcePerGame'] = 0
            record['hot'] = 0
            record['cold'] = 0
            record['lastupdated'] = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")

            if record['games'] >= min_games:
                print('Player added:', player_data['people'][0]['fullName'], flush=True)
                player_stats_skaters.append(record)
            else:
                print('Not enough games for:', player_data['people'][0]['fullName'], flush=True)
    return(player_stats_skaters, player_stats_goalies)

def get_skater_fantasy_ppg(gpg, apg, spg, bpg):
    goal_fpts = gpg * 8.5
    assist_fpts = apg * 5
    shots_fpts = spg * 1.5
    block_fpts = bpg * 1.3
    return (goal_fpts + assist_fpts + shots_fpts + block_fpts)

def get_goalie_fantasy_ppg(games, wins, saves, gaa, shutouts, ot):
    wins_per_game = (wins / games)
    saves_per_game = (saves / games)
    so_per_game = (shutouts / games)
    ot_per_game = (ot / games)

    wins_fpts = (wins_per_game * 6)
    saves_fpts = (saves_per_game * 0.7)
    gaa_fpts = (gaa * (-3.5))
    so_fpts = (so_per_game * 4)
    ot_fpts = (ot_per_game * 2)

    return(wins_fpts + saves_fpts + gaa_fpts + so_fpts + ot_fpts)
