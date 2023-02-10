from api_players import write_player_data
from api_schedule import write_game_schedule
from api_teams import write_team_data
from api_player_game_history import write_player_game_history_data
from skaters import add_skater_averages_to_csv, set_hot_cold

if __name__ == "__main__":
    print('Player write in progress...', flush=True)
    write_player_data()

    print('Schedule write in progress...', flush=True)
    write_game_schedule()

    print('Team write in progress...', flush=True)
    write_team_data()

    print('Writing player game history...', flush=True)
    write_player_game_history_data()

    print('Cleaning player data...', flush=True)
    add_skater_averages_to_csv()

    print('Who is hot, who is cold? Lets find out...', flush=True)
    set_hot_cold()
