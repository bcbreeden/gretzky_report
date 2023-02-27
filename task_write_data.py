from api_players import get_player_stats
from api_schedule import get_game_schedule
from api_teams import get_team_data
from api_player_game_history import get_player_game_history
from data_skaters import set_hot_cold
from script_utils import get_data_path, get_min_games, get_current_season
import pandas as pd

def write_player_data(player_data):
    skater_df = pd.DataFrame(player_data[0])
    goalie_df = pd.DataFrame(player_data[1])
    skater_df.to_csv(get_data_path('data_skater.csv'), encoding='utf-8', index=False)
    goalie_df.to_csv(get_data_path('data_goalie.csv'), encoding='utf-8', index=False)

def write_schedule_data(schedule_data):
    df = pd.DataFrame(schedule_data)
    df.to_csv(get_data_path('data_schedule.csv'), encoding='utf-8', index=False)

def write_team_data(team_data):
    df = pd.DataFrame(team_data)
    df.to_csv(get_data_path('data_teams.csv'), encoding='utf-8', index=False)

def write_player_game_history_data(game_history_data):
    skater_df = pd.DataFrame(game_history_data[0])
    goalie_df = pd.DataFrame(game_history_data[1])
    skater_df.to_csv(get_data_path('data_game_history_skater.csv'), encoding='utf-8', index=False)
    print('Skater game history file written successfully!', flush=True)
    goalie_df.to_csv(get_data_path('data_game_history_goalie.csv'), encoding='utf-8', index=False)
    print('Goalie game history file written successfully!', flush=True)


if __name__ == "__main__":
    print('Player write in progress...', flush=True)
    write_player_data(get_player_stats(get_min_games()))

    print('Schedule write in progress...', flush=True)
    write_schedule_data(get_game_schedule())

    print('Team write in progress...', flush=True)
    write_team_data(get_team_data())

    print('Writing player game history...', flush=True)
    write_player_game_history_data(get_player_game_history(get_current_season()))

    print('Who is hot, who is cold? Lets find out...', flush=True)
    set_hot_cold()
