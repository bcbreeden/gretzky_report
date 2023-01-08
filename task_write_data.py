from task_players import write_player_data, write_player_game_history_data
from task_schedule import write_game_schedule
from task_teams import write_team_data
from skaters import add_skater_averages_to_csv

if __name__ == "__main__":
    print('Player write in progress...', flush=True)
    write_player_data()

    print('Schedule write in progress...', flush=True)
    write_game_schedule()

    print('Team write in progress...', flush=True)
    write_team_data()

    print('Cleaning player data...', flush=True)
    add_skater_averages_to_csv()

    print('Writing player game history...', flush=True)
    write_player_game_history_data()