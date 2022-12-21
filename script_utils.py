MIN_GAMES = 10
DEV = True

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