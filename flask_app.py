from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from skaters import get_skater_data_by_id, get_skaters_data_by_team_id
from goalies import get_goalies_data_by_team_id
from teams import get_team_data_all, get_team_data_by_id, get_teams_data_by_team_ids, get_team_ids_all
from schedule import get_teams_playing_today

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
    if request.method == 'POST':
        selection = request.form['skater_selection']
        if selection == "All Skaters":
            SKATER_DATA = get_skaters_data_by_team_id(get_team_ids_all())
            return render_template('skaters.html',
                                    skaters = SKATER_DATA)
        elif selection == "Skaters Today":
            SKATER_DATA = get_skaters_data_by_team_id(get_teams_playing_today())
            return render_template('skaters.html',
                                    skaters = SKATER_DATA)
        else: 
            return render_template('skaters.html')
    else:
        return render_template('skaters.html')

@app.route('/skater_card/', methods=('GET', 'POST'))
def skater_card():
    if request.method == 'POST':
        skater_id = request.form['skater_id']
        skater_team_id = request.form['skater_team_id']
        print(skater_team_id)
        skater_team_data = get_team_data_by_id(skater_team_id)
        skater_data = get_skater_data_by_id(skater_id)
        return render_template('skater.html',
                                skater = skater_data,
                                teams = skater_team_data)
    else:
        return redirect(url_for('index'))

'''
Renders a template with the skater team selection form.
'''
@app.route('/skater_form/')
def skater_form():
    TEAMS_DATA = get_team_data_all()
    return render_template("skater_form.html",
                            teams = TEAMS_DATA)

'''
Renders the comparison page for teams.
'''
@app.route('/compare_teams/', methods=('GET', 'POST'))
def compare_teams():
    if request.method == 'POST':
        team_ids_get = request.form.getlist('team') # returned as strings
        team_ids = list(map(int, team_ids_get)) # cast to integer
        teams_data_by_id = get_teams_data_by_team_ids(team_ids)
        teams_data_all = get_team_data_all()
        return render_template('teams_comparison.html',
                        teams_all = teams_data_all,
                        teams = teams_data_by_id
        )
    else:
        teams_data_all = get_team_data_all()
        return render_template('teams_comparison.html',
                        teams_all = teams_data_all
        )

@app.route('/goalies_all/')
def goalies_all():
    GOALIES_DATA = get_goalies_data_by_team_id(get_team_ids_all())
    return render_template('goalies_all.html',
                            goalies = GOALIES_DATA)