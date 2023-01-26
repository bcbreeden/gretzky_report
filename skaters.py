import pandas as pd
from script_utils import get_min_games, get_data_path, get_hot_cold_dif

# DATA = pd.read_csv(get_data_path('data_skater.csv'), float_precision='round_trip')

def read_skater_data():
    return(pd.read_csv(get_data_path('data_skater.csv'), float_precision='round_trip'))

'''
Fetches skater data from the CSV file via a skater ids.
'''
def get_skater_data_by_id(player_id):
    DATA  = read_skater_data()
    skater = DATA.loc[DATA['id']==int(player_id)]
    return(skater)

'''
Fetches skater data from the CSV file via a list of team ids. The data is then returned in a list.
'''
def get_skaters_data_by_team_id(team_ids):
    DATA  = read_skater_data()
    skaters = DATA.loc[DATA['teamid'].isin(team_ids)]
    return(skaters)

def get_top_skaters(number, feature):
    DATA  = read_skater_data()
    skaters = DATA.sort_values(by=[feature])
    return(skaters)

'''
Calculates the nhl average for metrics: goals per game, assists per game, shots per game, and points per game.

These values are then added to the skater data. The skater data CSV file is opened, modified, and closed with the new data.
'''
def add_skater_averages_to_csv():
    DATA  = read_skater_data()

    # Goals per game average. We dont want players with less than the min games because they can skew the averages.
    wing_data_gpg = DATA.loc[(DATA['games'] >= get_min_games()) & ((DATA['position'] == 'Left Wing') | (DATA['position'] == 'Right Wing'))]
    wing_gpg_avg = wing_data_gpg['GPG'].mean()

    center_data_gpg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Center')]
    center_gpg_avg = center_data_gpg['GPG'].mean()

    defense_data_gpg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Defenseman')]
    defense_gpg_avg = defense_data_gpg['GPG'].mean()

    # Assists per game average
    wing_data_apg = DATA.loc[(DATA['games'] >= get_min_games()) & ((DATA['position'] == 'Left Wing') | (DATA['position'] == 'Right Wing'))]
    wing_apg_avg = wing_data_apg['APG'].mean()

    center_data_apg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Center')]
    center_apg_avg = center_data_apg['APG'].mean()

    defense_data_apg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Defenseman')]
    defense_apg_avg = defense_data_apg['APG'].mean()

    # Shots per game average
    wing_data_spg = DATA.loc[(DATA['games'] >= get_min_games()) & ((DATA['position'] == 'Left Wing') | (DATA['position'] == 'Right Wing'))]
    wing_spg_avg = wing_data_spg['SPG'].mean()

    center_data_spg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Center')]
    center_spg_avg = center_data_spg['SPG'].mean()

    defense_data_spg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Defenseman')]
    defense_spg_avg = defense_data_spg['SPG'].mean()

    #Points per game average 
    wing_data_ppg = DATA.loc[(DATA['games'] >= get_min_games()) & ((DATA['position'] == 'Left Wing') | (DATA['position'] == 'Right Wing'))]
    wing_ppg_avg = wing_data_ppg['PPG'].mean()

    center_data_ppg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Center')]
    center_ppg_avg = center_data_ppg['PPG'].mean()

    defense_data_ppg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Defenseman')]
    defense_ppg_avg = defense_data_ppg['PPG'].mean()

    # Blocks per game average
    wing_data_bpg = DATA.loc[(DATA['games'] >= get_min_games()) & ((DATA['position'] == 'Left Wing') | (DATA['position'] == 'Right Wing'))]
    wing_bpg_avg = wing_data_bpg['BPG'].mean()

    center_data_bpg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Center')]
    center_bpg_avg = center_data_bpg['BPG'].mean()

    defense_data_bpg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Defenseman')]
    defense_bpg_avg = defense_data_bpg['BPG'].mean()

    # Fantasy points per game average
    wing_data_fppg = DATA.loc[(DATA['games'] >= get_min_games()) & ((DATA['position'] == 'Left Wing') | (DATA['position'] == 'Right Wing'))]
    wing_fppg_avg = wing_data_fppg['FPPG'].mean()

    center_data_fppg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Center')]
    center_fppg_avg = center_data_fppg['FPPG'].mean()

    defense_data_fppg = DATA.loc[(DATA['games'] >= get_min_games()) & (DATA['position'] == 'Defenseman')]
    defense_fppg_avg = defense_data_fppg['FPPG'].mean()

    # Create new columns for metric differences and calculate the new values for said columns.
    data_add_df = DATA.assign(GPGDIF=0.0,APGDIF=0.0,SPGDIF=0.0, PPGDIF=0.0, BPGDIF=0.0)
    for index, row in data_add_df.iterrows():
        if row['games'] <= get_min_games():
            print('Minimum games not reached:', row['playername'])
            data_add_df = data_add_df.drop(index)
        else:
            if row['position'] == 'Defenseman':
                data_add_df.at[index,'GPGDIF'] = round((row['GPG'] - defense_gpg_avg), 2)
                data_add_df.at[index,'APGDIF'] = round((row['APG'] - defense_apg_avg), 2)
                data_add_df.at[index,'SPGDIF'] = round((row['SPG'] - defense_spg_avg), 2)
                data_add_df.at[index,'PPGDIF'] = round((row['PPG'] - defense_ppg_avg), 2)
                data_add_df.at[index,'BPGDIF'] = round((row['BPG'] - defense_bpg_avg), 2)
                data_add_df.at[index,'FPPGDIF'] = round((row['FPPG'] - defense_fppg_avg), 2)

            if row['position'] == ('Left Wing'):
                data_add_df.at[index,'GPGDIF'] = round((row['GPG'] - wing_gpg_avg), 2)
                data_add_df.at[index,'APGDIF'] = round((row['APG'] - wing_apg_avg), 2)
                data_add_df.at[index,'SPGDIF'] = round((row['SPG'] - wing_spg_avg), 2)
                data_add_df.at[index,'PPGDIF'] = round((row['PPG'] - wing_ppg_avg), 2)
                data_add_df.at[index,'BPGDIF'] = round((row['BPG'] - wing_bpg_avg), 2)
                data_add_df.at[index,'FPPGDIF'] = round((row['FPPG'] - wing_fppg_avg), 2)
            
            if row['position'] == ('Right Wing'):
                data_add_df.at[index,'GPGDIF'] = round((row['GPG'] - wing_gpg_avg), 2)
                data_add_df.at[index,'APGDIF'] = round((row['APG'] - wing_apg_avg), 2)
                data_add_df.at[index,'SPGDIF'] = round((row['SPG'] - wing_spg_avg), 2)
                data_add_df.at[index,'PPGDIF'] = round((row['PPG'] - wing_ppg_avg), 2)
                data_add_df.at[index,'BPGDIF'] = round((row['BPG'] - wing_bpg_avg), 2)
                data_add_df.at[index,'FPPGDIF'] = round((row['FPPG'] - wing_fppg_avg), 2)
            
            if row['position'] == 'Center':
                data_add_df.at[index,'GPGDIF'] = round((row['GPG'] - center_gpg_avg), 2)
                data_add_df.at[index,'APGDIF'] = round((row['APG'] - center_apg_avg), 2)
                data_add_df.at[index,'SPGDIF'] = round((row['SPG'] - center_spg_avg), 2)
                data_add_df.at[index,'PPGDIF'] = round((row['PPG'] - center_ppg_avg), 2)
                data_add_df.at[index,'BPGDIF'] = round((row['BPG'] - center_bpg_avg), 2)
                data_add_df.at[index,'FPPGDIF'] = round((row['FPPG'] - center_fppg_avg), 2)

    # Write the new DF to the CSV file.
    data_add_df.to_csv(get_data_path('data_skater.csv'), encoding='utf-8', index=False)

def set_hot_cold():
    skater_data_all = read_skater_data()
    skater_game_history = pd.read_csv(get_data_path('data_game_history_skater.csv'), float_precision='round_trip')
    for index, skater in skater_data_all.iterrows():
        game_history = skater_game_history.loc[skater_game_history['player_id'] == skater['id']]
        fantasy_avg_5_games = game_history['fantasy_points'].mean()
        difference = (fantasy_avg_5_games - skater['FPPG'])
        if difference >= get_hot_cold_dif():
            skater_data_all.at[index,'hot'] = 1
        elif difference <= (get_hot_cold_dif() - (get_hot_cold_dif() * 2)):
            skater_data_all.at[index,'cold'] = 1
    skater_data_all.to_csv(get_data_path('data_skater.csv'), encoding='utf-8', index=False)