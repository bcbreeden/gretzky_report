from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json
from data_skaters import get_skater_data_by_id, get_skaters_data_by_team_id
from data_goalies import get_goalies_data_by_team_id, get_goalie_data_by_id
from data_teams import get_team_data_all, get_team_data_by_id, get_teams_data_by_team_ids, get_team_ids_all
from data_schedule import get_teams_playing_today, get_next_opponent, get_last_opponent
from data_player_game_history import get_skater_history_by_id, get_skater_plot_data, get_goalie_history_by_id, get_goalie_plot_data

app = Flask(__name__)
app.config["DEBUG"] = True

'''
Renders the index template.
'''
@app.route('/')
def index():
    return render_template('index.html')                        

@app.route('/skaters/', methods=('GET', 'POST'))
def skaters():
    teams_data_all = get_team_data_all()
    team_ids_playing_today = get_teams_playing_today()
    team_ids_all = get_team_ids_all()
    if request.method == 'POST':
        team_ids_get = request.form.getlist('team') # returned as strings
        team_ids = list(map(int, team_ids_get)) # cast to integer
        SKATER_DATA = get_skaters_data_by_team_id(team_ids)
        return render_template('skaters.html',
                                skaters = SKATER_DATA,
                                teams_all = teams_data_all,
                                team_ids_playing_today = json.dumps(team_ids_playing_today),
                                team_ids_all = json.dumps(team_ids_all))
    else:
        return render_template('skaters.html',
                                teams_all = teams_data_all,
                                team_ids_playing_today = json.dumps(team_ids_playing_today),
                                team_ids_all = json.dumps(team_ids_all))

@app.route('/player_details/', methods=('GET', 'POST'))
def player_details():
    if request.method == 'POST':
        offseason = False
        player_id = request.form['player_id']
        player_team_id = int(request.form['player_team_id'])
        position = request.form['position']
        try:
            opponent_team_id = get_next_opponent(player_team_id)
        except IndexError:
            print('There is not a game coming up, using last opponent.', flush=True)
            offseason = True
            opponent_team_id = get_last_opponent(player_team_id)
        teams_data_by_id = get_teams_data_by_team_ids([player_team_id, opponent_team_id])

        # Skater
        if position == 's':
            skater_data = get_skater_data_by_id(player_id)
            skater_history_data = get_skater_history_by_id(player_id)
            max_y_plot_value = int(skater_history_data['fantasy_points'].max()+5)
            skater_history_plot_data = get_skater_plot_data(skater_history_data)
            return render_template('player_details.html',
                                    player = skater_data,
                                    skater_history = skater_history_data,
                                    plot_opponents = skater_history_plot_data[0],
                                    plot_fantasy_points = skater_history_plot_data[1],
                                    teams = teams_data_by_id,
                                    position = position,
                                    offseason = offseason,
                                    max_y_plot_value = max_y_plot_value)
        # Goalie
        elif position == 'g':
            goalie_data = get_goalie_data_by_id(player_id)
            goalie_history_data = get_goalie_history_by_id(player_id)
            max_y_plot_value = int(goalie_history_data['fantasy_points'].max()+5)
            goalie_history_plot_data = get_goalie_plot_data(goalie_history_data)
            return render_template('player_details.html',
                                    player = goalie_data,
                                    goalie_history = goalie_history_data,
                                    plot_opponents = goalie_history_plot_data[0],
                                    plot_fantasy_points = goalie_history_plot_data[1],
                                    teams = teams_data_by_id,
                                    position = position,
                                    offseason = offseason,
                                    max_y_plot_value = max_y_plot_value)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

'''
Renders the comparison page for teams.
'''
@app.route('/compare_teams/', methods=('GET', 'POST'))
def compare_teams():
    teams_data_all = get_team_data_all()
    team_ids_playing_today = get_teams_playing_today()
    team_ids_all = get_team_ids_all()
    if request.method == 'POST':
        team_ids_get = request.form.getlist('team') # returned as strings
        team_ids = list(map(int, team_ids_get)) # cast to integer
        teams_data_by_id = get_teams_data_by_team_ids(team_ids)
        teams_data_all = get_team_data_all()
        return render_template('teams_comparison.html',
                        teams_all = teams_data_all,
                        teams = teams_data_by_id,
                        team_ids_playing_today = json.dumps(team_ids_playing_today),
                        team_ids_all = json.dumps(team_ids_all))
    else:
        teams_data_all = get_team_data_all()
        return render_template('teams_comparison.html',
                        teams_all = teams_data_all,
                        team_ids_playing_today = json.dumps(team_ids_playing_today),
                        team_ids_all = json.dumps(team_ids_all))

@app.route('/goalies/', methods=('GET', 'POST'))
def goalies():
    teams_data_all = get_team_data_all()
    team_ids_playing_today = get_teams_playing_today()
    team_ids_all = get_team_ids_all()
    if request.method == 'POST':
        team_ids_get = request.form.getlist('team') # returned as strings
        team_ids = list(map(int, team_ids_get)) # cast to integer
        GOALIE_DATA = get_goalies_data_by_team_id(team_ids)
        return render_template('goalies.html',
                                goalies = GOALIE_DATA,
                                teams_all = teams_data_all,
                                team_ids_playing_today = json.dumps(team_ids_playing_today),
                                team_ids_all = json.dumps(team_ids_all))
    else:
        return render_template('goalies.html',
                                teams_all = teams_data_all,
                                team_ids_playing_today = json.dumps(team_ids_playing_today),
                                team_ids_all = json.dumps(team_ids_all))
