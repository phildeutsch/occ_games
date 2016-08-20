from tf import models
import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as po

player = models.Player.objects.get(last_name="Deutsch")

matches = [x.match_set.all() for x in player.team_set.all()]
matches = [item for sublist in matches for item in sublist]
matches = [x for x in matches if x.matchtype==gametype]
matches = sorted(matches, key=lambda x:x.played_date, reverse=True)

dates = [m.played_date for m in matches]
elo11 = [m.team1_elos_to_int()[0] for m in matches]
elo12 = [m.team1_elos_to_int()[1] for m in matches]
elo21 = [m.team2_elos_to_int()[0] for m in matches]
elo22 = [m.team2_elos_to_int()[1] for m in matches]

t1  = [player in m.teams.order_by('id')[0].players.all() for m in matches]
p11 = [player == m.teams.order_by('id')[0].players.order_by('id')[0] for m in matches]
t2  = [player in m.teams.order_by('id')[1].players.all() for m in matches]
p21 = [player == m.teams.order_by('id')[1].players.order_by('id')[0] for m in matches]

id = []
elo11 = []
elo12 = []
elo21 = []
elo22 = []
p11 = []
p12 = []
p21 = []
p22 = []
win = []

for m in matches:
    id.append(m.id)
    win.append(player in m.get_winner().players.all())
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

df = pd.DataFrame({'date':dates, 'team':1, 'player':1, 'elo': elo11, 'name': p11, 'id':id, 'win':win})
df = df.append(pd.DataFrame({'date':dates, 'team':1, 'player':2, 'elo': elo12, 'name'  : p12, 'id':id, 'win':win}))
df = df.append(pd.DataFrame({'date':dates, 'team':2, 'player':1, 'elo': elo21, 'name'  : p21, 'id':id, 'win':win}))
df = df.append(pd.DataFrame({'date':dates, 'team':2, 'player':2, 'elo': elo22, 'name'  : p22, 'id':id, 'win':win}))
df.sort_values(by='date', inplace=True)
df['date'] = df['date'].apply(lambda x: x.date())
df = df.query("name != 'NA'")

df_player_team = df[df.name==player.full_name][['id', 'team']]
df_player_team['player_team'] = True

df = pd.merge(df, df_player_team, on=['id', 'team'], how='outer')
df.loc[df.player_team != True, 'player_team'] = False

# Elo plot
df_elo = df[df.name==player.full_name].groupby("date").agg({"elo" : min})
data = [go.Scatter(
    x = df_elo.index.values,
    y = df_elo['elo'].values
)]
layout = go.Layout()
fig = go.Figure(data=data, layout=layout)
plot_div = po.plot(fig, include_plotlyjs=False, output_type='div')

# Rivals plot
df_rivals = (df[df.player_team==False].groupby("name")
    .agg({"name" : "count", "win":sum})
    .rename(columns={"name":"count", "win":"wins"}))
df_rivals['win_perc'] = round(100 * df_rivals['wins'] / df_rivals['count'])
df_rivals['losses'] = df_rivals['count'] - df_rivals['wins']
df_rivals.sort('count', ascending=True, inplace=True)
df_rivals = df_rivals.iloc[:10]

trace_wins = go.Bar(
            x=df_rivals['wins'].values,
            y=df_rivals.index.values,
            text = ["Win Rate: " + str(x) + "%" for x in df_rivals['win_perc'].values],
            orientation = 'h',
            name='Wins'
)
trace_losses = go.Bar(
            x=df_rivals['losses'].values,
            y=df_rivals.index.values,
            orientation = 'h',
            name='Losses',
            marker=dict(
                color='rgb(204,204,204)',
                )
)
data = [trace_wins, trace_losses]
layout = go.Layout(
  margin={"l":200},
  barmode='stack'
  )
fig = go.Figure(data=data, layout=layout)
plot_rivals = po.plot(fig, include_plotlyjs=False, output_type='div')


plot_div = plot_div.replace(': true',  ': false')
plot_rivals = plot_rivals.replace(': true',  ': false')
