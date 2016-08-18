from tf import models
import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as po

player = models.Player.objects.get(last_name="Deutsch")
tf_matches = [x.match_set.all() for x in player.team_set.all()]
tf_matches = [item for sublist in tf_matches for item in sublist]
tf_matches = [x for x in tf_matches if x.matchtype=='TF']
tf_matches = sorted(tf_matches, key=lambda x:x.played_date, reverse=True)

dates = [m.played_date for m in tf_matches]
elo11 = [m.team1_elos_to_int()[0] for m in tf_matches]
elo12 = [m.team1_elos_to_int()[1] for m in tf_matches]
elo21 = [m.team2_elos_to_int()[0] for m in tf_matches]
elo22 = [m.team2_elos_to_int()[1] for m in tf_matches]

t1  = [player in m.teams.order_by('id')[0].players.all() for m in tf_matches]
p11 = [player == m.teams.order_by('id')[0].players.order_by('id')[0] for m in tf_matches]
t2  = [player in m.teams.order_by('id')[1].players.all() for m in tf_matches]
p21 = [player == m.teams.order_by('id')[1].players.order_by('id')[0] for m in tf_matches]

elo11 = elo12 = elo21 = elo22 = []
p11 = p12 = p21 = p22 = []

for m in [tf_matches[0]]:
    print(m.id)
    elo11.append(m.team1_elos_to_int()[0])
    elo21.append(m.team2_elos_to_int()[0])
    p11.append(m.teams.order_by('id').all()[0].players.order_by('id')[0].full_name)
    p21.append(m.teams.order_by('id').all()[1].players.order_by('id')[0].full_name)
    if m.team1_elos_to_int()[1] != 0:
        elo12.append(m.team1_elos_to_int()[1])
        p12.append(m.teams.order_by('id').all()[0].players.order_by('id')[1].full_name)
    else:
        elo12.append(0)
        p12.append('NA')
    if m.team2_elos_to_int()[1] != 0:
        elo22.append(m.team2_elos_to_int()[1])
        p22.append(m.teams.order_by('id').all()[1].players.order_by('id')[1].full_name)
    else:
        elo22.append(0)
        p22.append('NA')

df = pd.DataFrame({'date':dates,
'elo11': elo11,
'elo12': elo12,
'elo21': elo21,
'elo22': elo22,
'p11'  : p11,
'p12'  : p12,
'p21'  : p21,
'p22'  : p22
})
df.sort_values(by='date', inplace=True)
df['date'] = df['date'].apply(lambda x: x.date())

is_p11 = df['t1'] & df['p11']
is_p12 = df['t1'] & -df['p11']
is_p21 = df['t2'] & df['p21']
is_p22 = df['t2'] & -df['p21']

df['elo'] = 0
df.loc[is_p11, 'elo'] = df['elo11'][is_p11]
df.loc[is_p12, 'elo'] = df['elo12'][is_p12]
df.loc[is_p21, 'elo'] = df['elo21'][is_p21]
df.loc[is_p22, 'elo'] = df['elo22'][is_p22]

df_elo = df.groupby("date").agg({"elo" : min})

# Create a trace
trace = go.Scatter(
    x = df_elo.index.values,
    y = df_elo['elo'].values
)

data = [trace]
plot_div = po.plot(data, include_plotlyjs=False, output_type='div')
