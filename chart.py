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


df = pd.DataFrame({'date':dates,
'elo11': elo11,
'elo12': elo12,
'elo21': elo21,
'elo22': elo22,
't1': t1,
'p11': p11,
't2': t2,
'p21': p21,
})
df.sort_values(by='date', inplace=True)
df['date'] = df['date'].apply(lambda x: x.date())

p11 = df['t1'] & df['p11']
p12 = df['t1'] & -df['p11']
p21 = df['t2'] & df['p21']
p22 = df['t2'] & -df['p21']

df['elo'] = 0
df.loc[p11, 'elo'] = df['elo11'][p11]
df.loc[p12, 'elo'] = df['elo12'][p12]
df.loc[p21, 'elo'] = df['elo21'][p21]
df.loc[p22, 'elo'] = df['elo22'][p22]

df = df.groupby("date").agg({"elo" : min})

# Create a trace
trace = go.Scatter(
    x = df.index.values,
    y = df['elo'].values
)

data = [trace]
plot_div = po.plot(data, include_plotlyjs=False, output_type='div')
