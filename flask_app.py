from flask import Flask, render_template, request, redirect, url_for
# from flask_caching import Cache
import pandas as pd
from skaters import get_skater_data_by_id, get_skaters_data_by_team_id, get_top_skaters
from teams import get_team_data_all, get_team_data_by_id, get_teams_data_by_team_ids
from schedule import get_teams_playing_today

app = Flask(__name__)
# cache = Cache()

app.config["DEBUG"] = True
app.config["CACHE_TYPE"] = 'simple'
# cache.init_app(app)

'''
Renders the index template.
'''
@app.route('/')
def index():
    return render_template('index.html')                        

@app.route('/skaters_today/')
def skaters_today():
    SKATER_DATA = get_skaters_data_by_team_id(get_teams_playing_today())
    features = ['playername', 'teamid', 'currentteam', 'position', 'GPG', 'GPGDIF', 'APG', 'APGDIF', 'SPG', 'SPGDIF', 'PPG', 'PPGDIF', 'BPG', 'timeonicepergame', 'id']
    view_data = SKATER_DATA[features]
    return render_template('skaters_today.html',
                            skaters = view_data,
                            headers = view_data.columns.drop(['GPGDIF', 'APGDIF', 'SPGDIF', 'PPGDIF', 'id', 'teamid'])) #We dont need these column headers


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
Renders the results from the skater form into a table.
'''
# @app.route('/skater_results/', methods=('GET', 'POST'))
# def skater_results():
#     if request.method == 'POST':
#         form_data = request.form.getlist('team')
#         ids = [eval(i) for i in form_data]
#         SKATER_DATA = get_skaters_data_by_team_id(ids)
#         features = ['playername', 'currentteam', 'position', 'GPG', 'GPGDIF', 'APG', 'APGDIF', 'SPG', 'SPGDIF', 'PPG', 'PPGDIF', 'BPG', 'timeonicepergame', 'id']
#         view_data = SKATER_DATA[features]
#         print(view_data)
#         return render_template('skater_results_table.html',
#                             skaters = view_data,
#                             headers = view_data.columns.drop(['GPGDIF', 'APGDIF', 'SPGDIF', 'PPGDIF', 'id']))
                                
#     else:
#         return redirect(url_for('index'))

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

# @cache.cached(timeout=260, key_prefix='function')
# def function():
#     '''Caches the data that is updated every ~5 minutes.'''
#     data = 5
#     return data