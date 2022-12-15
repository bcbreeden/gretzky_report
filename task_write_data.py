from task_players import write_player_data
from task_schedule import write_game_schedule
from task_teams import write_team_data

if __name__ == "__main__":
    print('Player write in progress...')
    write_player_data()

    print('Schedule write in progress...')
    write_game_schedule()

    print('Team write in progress...')
    write_team_data()