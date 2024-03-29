import json
import requests
from datetime import datetime, timedelta

'''
Calls the api and formats a list of dictionaries containing the game schedule.
'''
def get_game_schedule(season):
    games_data_all = []
    request_string = 'https://statsapi.web.nhl.com/api/v1/schedule?season={}'.format(season)
    schedule_data = json.loads(requests.get(request_string).text)
    dates = schedule_data['dates']
    for date in dates:
        games = date['games']
        for game in games:
            game_data = {}
            game_data['id'] = game['gamePk']
            game_data['gamedate'] = format_date_time(game['gameDate'])[0]
            game_data['gametime'] = format_date_time(game['gameDate'])[1]
            game_data['homeid'] = game['teams']['home']['team']['id']
            game_data['awayid'] = game['teams']['away']['team']['id']
            games_data_all.append(game_data)
    return(games_data_all)

'''
Returns the date and time in a list.

UTC -> EST
'''
def format_date_time(date_string):
    results = []
    dt_string_formatted = date_string.replace('T', ' ')
    dt_string_formatted = dt_string_formatted.replace('Z', ' UTC')

    dt_obj = datetime.strptime(dt_string_formatted, '%Y-%m-%d %H:%M:%S %Z')
    est = dt_obj - timedelta(hours=4)

    # [date, time]
    results.append(est.strftime('%Y-%m-%d'))
    results.append(est.strftime('%H:%M:%S'))

    return(results)