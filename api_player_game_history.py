from api_players import get_player_ids
from data_teams import read_teams_data
import requests
import json

def get_player_game_history(current_season):
    player_ids = get_player_ids()
    team_data = read_teams_data()
    player_game_history_skaters = []
    player_game_history_goalies = []
    for player_id in player_ids:
        print('Player ID:', player_id, flush=True)
        request_string = 'https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=gameLog&season={}'.format(player_id, current_season)
        player_game_history_data = json.loads(requests.get(request_string).text)
        games = player_game_history_data['stats'][0]['splits']
        for game in games[:5]: #last 5 games
            opponent_record = team_data.loc[team_data['id'] == game['opponent']['id']]
            # print(type(opponent_record.iloc[0]['abbreviation']))
            record= {}
            record['player_id'] = player_id
            record['date'] = game['date']
            record['home_game'] = game['isHome']
            if game['isHome'] == True:
                record['opp'] = opponent_record.iloc[0]['abbreviation']
            else:
                record['opp'] = '@' + opponent_record.iloc[0]['abbreviation']
            record['TOI'] = game['stat']['timeOnIce']
            try:
                record['assists'] = game['stat']['assists']
                record['goals'] = game['stat']['goals']
                record['shots'] = game['stat']['shots']
                record['PPTOI'] = game['stat']['powerPlayTimeOnIce']
                record['blocks'] = game['stat']['blocked']
                record['fantasy_points'] = get_skater_fantasy_points(record['goals'], record['assists'], record['shots'], record['blocks'])
                player_game_history_skaters.append(record)
                print('Skater record add for {} {}.'.format(player_id, record['date']), flush=True)
            except KeyError:
                try:
                    record['saves'] = game['stat']['saves']
                    record['save_perc'] = game['stat']['savePercentage']
                    record['goals_against'] = game['stat']['goalsAgainst']
                    record['shots_against'] = game['stat']['shotsAgainst']
                    record['decision'] = game['stat']['decision']
                    record['shutout'] = game['stat']['shutouts']
                    record['save_pctg'] = game['stat']['savePercentage']
                    record['ot'] = game['stat']['ot']
                    record['fantasy_points'] = get_goalie_fantasy_points(
                        record['decision'],
                        record['saves'],
                        record['goals_against'],
                        record['shutout'],
                        record['ot']
                    )
                    player_game_history_goalies.append(record)
                    print('Goalie record add for {}.'.format(player_id), flush=True)
                except Exception:
                    print('Data not found or data corrupt for this game. Skipping record', flush=True)

    return(player_game_history_skaters, player_game_history_goalies)

def get_skater_fantasy_points(goals, assists, shots, blocks):
    score = (goals * 8.5) + (assists * 5) + (shots * 1.5) + (blocks * 1.3)
    score = (score + 3) if (goals >=3) else score #Hat Trick Bonus
    score = (score + 3) if (shots >=5) else score #Shooter Bonus
    score = (score + 3) if (blocks >=3) else score #Blocker Bonus
    score = (score + 3) if ((goals + assists) >= 3) else score #Points Bonus
    return score

def get_goalie_fantasy_points(decision, saves, goals_against, shutout, ot):
    score = (saves * 0.7) + (goals_against * (-3.5))
    score = (score + 6) if (decision == 'W') else score
    score = (score + 4) if (shutout == 1) else score
    score = (score + 2) if (ot == 1) else score
    return score