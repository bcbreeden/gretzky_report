import json
import requests

# TODO: Write function to write to CSV.
'''
A helper function to notify get_game_plays when it should check for player ids.

These play types have player data associated with it.
'''
def plays_with_players():
    return ['FACEOFF',
            'HIT',
            'GIVEAWAY',
            'GOAL',
            'SHOT',
            'MISSED_SHOT',
            'TAKEAWAY',
            'FIGHT',
            'PENALTY']

'''
Pulls all of the plays for a given game id. For

Return is formatted as a list of dictionaries for the configured features.
'''
def get_game_plays(game_id):
    # print(game_id)
    request_string = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(game_id)
    game_detailed = json.loads(requests.get(request_string).text)
    plays = game_detailed['liveData']['plays']['allPlays']
    records = []
    for play in plays:
        play_data = {}
        play_data['play_id'] = int(str(game_id) + str(play['about']['eventId']))
        play_data['game_id'] = game_id
        play_data['event_id'] = play['about']['eventId']
        play_data['event_type_id'] = play['result']['eventTypeId']
        play_data['description'] = play['result']['description']
        play_data['time_stamp'] = play['about']['dateTime']
        play_data['period'] = play['about']['period']
        play_data['period_time'] = play['about']['periodTime']
        play_data['period_time_remaining'] = play['about']['periodTimeRemaining']

        if play['result']['eventTypeId'] in plays_with_players():
            players = play['players']
            index = 0
            for player in players:
                column = 'player_{}_id'.format(index)
                play_data[column] = player['player']['id']
                index += 1

        records.append(play_data)
        print('Play {} has been added to the records list.'.format(play_data['play_id']))

    
    return(records)