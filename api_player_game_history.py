from script_utils import get_data_path, get_current_season, get_hot_cold_dif
from api_players import get_player_ids
import pandas as pd
import requests
import json

def get_player_game_history():
    # GAMES_NEEDED = 5
    player_ids = get_player_ids()
    # player_ids = [8477970]

    player_game_history_skaters = []
    player_game_history_goalies = []
    for player_id in player_ids:
        print('Player ID:', player_id, flush=True)
        request_string = 'https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=gameLog&season={}'.format(player_id, get_current_season())
        player_game_history_data = json.loads(requests.get(request_string).text)
        games = player_game_history_data['stats'][0]['splits']
        for game in games[:5]: #last 5 games
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
                record['blocks'] = game['stat']['blocked']
                record['fantasy_points'] = get_game_fantasy_points(record['goals'], record['assists'], record['shots'], record['blocks'])
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

def get_game_fantasy_points(goals, assists, shots, blocks):
    score = (goals * 8.5) + (assists * 5) + (shots * 1.5) + (blocks * 1.3)
    score = (score + 3) if (goals >=3) else score #Hat Trick Bonus
    score = (score + 3) if (shots >=5) else score #Shooter Bonus
    score = (score + 3) if (blocks >=3) else score #Blocker Bonus
    score = (score + 3) if ((goals + assists) >= 3) else score #Points Bonus
    return score