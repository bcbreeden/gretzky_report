MIN_GAMES = 0
DEV = True
CURRENT_SEASON = '20222023'
HOT_COLD_DIF = 5

'''
Gets the minimum game requirement
'''
def get_min_games():
    return MIN_GAMES

'''
Sets the data url path depending in the DEV value.

True -> Route for local development
False -> Route for prod environment.
'''
def get_data_path(file_name):
    if DEV == True:
        return('static/data/{}'.format(file_name))
    else:
        return('/home/breedenb/pyhl-io/static/data/{}'.format(file_name))

'''
Gets the current season as a string
'''
def get_current_season():
    return CURRENT_SEASON

'''
For a player to be on a hot streak: their average fantasy points over the last 5 games needs to be N points higher than their standing average.

For a player to be on a cold streak: their average fantasy points over the last 5 games needs to be N points lower than their standing average.
'''
def get_hot_cold_dif():
    return HOT_COLD_DIF
