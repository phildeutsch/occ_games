from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import TfMatch, FifaMatch, Player, Team
from .forms import TfNewPlayerForm, TfNewMatchForm, FifaNewMatchForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import datetime
import config
import re
import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as po

def plot_elo(player, gametype):
    try:
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
        single_game = []

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
            if m.team2_elos_to_int()[1] == 0 and m.team1_elos_to_int()[1] ==0:
                single_game.append(True)
            else:
                single_game.append(False)

        df = pd.DataFrame({'date':dates, 'team':1, 'player':1, 'elo': elo11, 'name': p11, 'id':id, 'win':win, 'singles':single_game})
        df = df.append(pd.DataFrame({'date':dates, 'team':1, 'player':2, 'elo': elo12, 'name'  : p12, 'id':id, 'win':win, 'singles':single_game}))
        df = df.append(pd.DataFrame({'date':dates, 'team':2, 'player':1, 'elo': elo21, 'name'  : p21, 'id':id, 'win':win, 'singles':single_game}))
        df = df.append(pd.DataFrame({'date':dates, 'team':2, 'player':2, 'elo': elo22, 'name'  : p22, 'id':id, 'win':win, 'singles':single_game}))
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
        layout = go.Layout(
            xaxis=dict(
                tickfont=dict(
                    family='Arial, sans-serif',
                    size=14,
                    color='black'
                ),
            ),
            yaxis=dict(
                title = "Elo Score",
                titlefont=dict(
                    family='Arial, sans-serif',
                    size=18,
                    color='black'
                ),
                tickfont=dict(
                    family='Arial, sans-serif',
                    size=14,
                    color='black'
                )
            )
        )
        fig = go.Figure(data=data, layout=layout)
        plot_div = po.plot(fig, include_plotlyjs=False, output_type='div')

        # Rivals plot
        df_rivals = (df[(df.player_team==False) & (df.singles==True)].groupby("name")
            .agg({"name" : "count", "win":sum})
            .rename(columns={"name":"count", "win":"wins"}))
        df_rivals['win_perc'] = round(100 * df_rivals['wins'] / df_rivals['count'])
        df_rivals['losses'] = df_rivals['count'] - df_rivals['wins']
        df_rivals.sort('count', ascending=False, inplace=True)
        df_rivals = df_rivals.iloc[:5]

        trace_wins = go.Bar(
                    x=np.flipud(df_rivals['wins'].values),
                    y=np.flipud(df_rivals.index.values),
                    text = ["Win Rate: " + str(x) + "%" for x in np.flipud(df_rivals['win_perc'].values)],
                    orientation = 'h',
                    name='Wins'
        )
        trace_losses = go.Bar(
                    x=np.flipud(df_rivals['losses'].values),
                    y=np.flipud(df_rivals.index.values),
                    orientation = 'h',
                    name='Losses',
                    marker=dict(
                        color='rgb(204,204,204)',
                        )
        )
        data = [trace_wins, trace_losses]
        layout = go.Layout(
          margin={"l":200},
          barmode='stack',
          xaxis=dict(
              tickfont=dict(
                  family='Arial, sans-serif',
                  size=14,
                  color='black'
              ),
          ),
          yaxis=dict(
              tickfont=dict(
                  family='Arial, sans-serif',
                  size=14,
                  color='black'
              )
          )
        )
        fig = go.Figure(data=data, layout=layout)
        plot_rivals = po.plot(fig, include_plotlyjs=False, output_type='div')

        plot_div = plot_div.replace(': true',  ': false')
        plot_rivals = plot_rivals.replace(': true',  ': false')
    except:
        plot_div = plot_rivals = ""

    return [plot_div, plot_rivals]

def get_team(player1, player2):
    if player1.id > player2.id:
        tmp = player1
        player1 = player2
        player2 = tmp
    try:
        if player1.id == 0:
            team = Team.objects.filter(players=player2).filter(is_single_player=True)[0]
        else:
            team = Team.objects.filter(players=player1).filter(players=player2)[0]
    except IndexError:
        team = Team()
        team.save()
        if player1.id != 0:
            team.players.add(player1)
        if player2.id != 0:
            team.players.add(player2)
        team.is_single_player = True if len(team.players.all())==1 else False
        team.save()
    return team

def home(request):
    cutoff_date = timezone.now() - datetime.timedelta(days=30)
    tf_players_ordered = (Player.objects.all().
                        filter(id__gt=0).
                        filter(tf_last_played__gt=cutoff_date).
                        filter(tf_matches_played__gt=0).
                        order_by('-tf_player_elo')[:config.LEAGUE_LENGTH])
    fifa_players_ordered = (Player.objects.all().
                        filter(id__gt=0).
                        filter(fifa_last_played__gt=cutoff_date).
                        filter(fifa_matches_played__gt=0).
                        order_by('-fifa_player_elo')[:config.LEAGUE_LENGTH])

    return render(request, "tf/home.html", {'user'                 : request.user,
                                            'fifa_players_ordered' : fifa_players_ordered,
                                            'tf_players_ordered'   : tf_players_ordered})

def player_new(request):
    if request.method == "POST":
        new_player_form = TfNewPlayerForm(request.POST)
        if new_player_form.is_valid():
            player = new_player_form.save(commit=False)
            player.full_name = player.first_name + ' ' + player.last_name
            player.save()
            return redirect('home')
    else:
        new_player_form = TfNewPlayerForm()
    return render(request, 'tf/add_player.html', {'form': new_player_form})

def player_league(request):
    tf_players_ordered = Player.objects.all().filter(id__gt=0).filter(tf_matches_played__gt=0).order_by('-tf_player_elo')
    fifa_players_ordered = Player.objects.all().filter(id__gt=0).filter(fifa_matches_played__gt=0).order_by('-fifa_player_elo')

    return render(request, "tf/player_league.html", {'tf_players_ordered':tf_players_ordered, 'fifa_players_ordered':fifa_players_ordered})

def faq(request):
    return render(request, "tf/faq.html",{})

def rules(request):
    return render(request, "tf/rules.html",{})

def register(request):
    print("request " + request.method)
    if request.method == "POST":
        user_form = UserForm(request.POST, prefix="register")
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.email = user_form['username']
            user.save()
            return redirect('home')
    else:
        user_form = UserForm(prefix="register")

    return render(request, "tf/registration/register.html", {'user_form' : user_form})

def tf_games(request):
    if request.user.is_superuser:
        su = True
        tf_matches = TfMatch.objects.filter(season=config.SEASON).order_by('-played_date').all()

        plot_div = ""
        plot_rivals = ""

    else:
        su = False
        player = request.user.player

        tf_matches = [x.match_set.all() for x in player.team_set.all()]
        tf_matches = [item for sublist in tf_matches for item in sublist]
        tf_matches = [x for x in tf_matches if x.matchtype=='TF']
        tf_matches = sorted(tf_matches, key=lambda x:x.played_date, reverse=True)
        tf_wins = [player in m.get_winner().players.all() for m in tf_matches]

        plot_div, plot_rivals = plot_elo(player, 'TF')

    tf = []
    i = 0
    for match in tf_matches:
        m = {}
        m['played_date'] = match.played_date
        m['winner'] = match.get_winner().prettyprint()
        m['loser'] = match.get_loser().prettyprint()
        m['winner_elos'] = match.print_winner_elos()
        m['winner_elo_change'] = match.get_winner_elo_change()
        m['winner_score'] = match.get_winner_score()
        m['loser_elos'] = match.print_loser_elos()
        m['loser_elo_change'] = match.get_loser_elo_change()
        m['loser_score'] = match.get_loser_score()
        if not request.user.is_superuser:
            m['win'] = tf_wins[i]==True
        tf.append(m)
        i = i + 1

    return render(request, "tf/tf_games.html", {'tf_matches' : tf,
                                                'su' : su,
                                                'plot_div':plot_div,
                                                'plot_rivals':plot_rivals})

def fifa_games(request):
    if request.user.is_superuser:
        su = True
        fifa_matches = FifaMatch.objects.filter(season=config.SEASON).order_by('-played_date').all()

        plot_div = ""
        plot_rivals = ""

    else:
        su = False
        player = request.user.player

        fifa_matches = [x.match_set.all() for x in player.team_set.all()]
        fifa_matches = [item for sublist in fifa_matches for item in sublist]
        fifa_matches = [x for x in fifa_matches if x.matchtype=='FF']
        fifa_matches = sorted(fifa_matches, key=lambda x:x.played_date, reverse=True)
        fifa_wins = [player in m.get_winner().players.all() for m in fifa_matches]

        plot_div, plot_rivals = plot_elo(player, 'FF')

    fifa = []
    i = 0
    for match in fifa_matches:
        m = {}
        m['played_date'] = match.played_date
        m['winner'] = match.get_winner().prettyprint()
        m['loser'] = match.get_loser().prettyprint()
        m['winner_elos'] = match.print_winner_elos()
        m['winner_elo_change'] = match.get_winner_elo_change()
        m['winner_score'] = match.get_winner_score()
        m['loser_elos'] = match.print_loser_elos()
        m['loser_elo_change'] = match.get_loser_elo_change()
        m['loser_score'] = match.get_loser_score()
        if not request.user.is_superuser:
            m['win'] = fifa_wins[i]==True
        fifa.append(m)
        i = i + 1

    return render(request, "tf/fifa_games.html", {'fifa_matches' : fifa,
                                                    'su' : su,
                                                    'plot_div':plot_div,
                                                    'plot_rivals':plot_rivals})

def enter_player(request):
    if request.method == "POST":
        player_form = TfNewPlayerForm(request.POST)
        if player_form.is_valid():
            player = player_form.save(commit=False)
            player.full_name = player.first_name + ' ' + player.last_name
            player.save()
            return redirect('home')
    else:
        player_form = TfNewPlayerForm()

    return render(request, "tf/enter_player.html", {'player_form' : player_form})

def enter_tf_match(request):
    if request.method == "POST":
        match_form = TfNewMatchForm(request.POST, request=request)
        if match_form.is_valid():
            team1_player1 = match_form.cleaned_data['team1_player1']
            team1_player2 = match_form.cleaned_data['team1_player2']
            team1_score = match_form.cleaned_data['team1_score']

            team2_player1 = match_form.cleaned_data['team2_player1']
            team2_player2 = match_form.cleaned_data['team2_player2']
            team2_score = match_form.cleaned_data['team2_score']

            team1 = get_team(team1_player1, team1_player2)
            team2 = get_team(team2_player1, team2_player2)

            if team1.id < team2.id:
                scores = str(team1_score) + ' ' + str(team2_score)
            else:
                scores = str(team2_score) + ' ' + str(team1_score)

            match = TfMatch(scores=scores, played_date=timezone.now())
            match.save()
            match.teams.add(team1, team2)
            match.save()

            team1.tf_team_matches_played += 1
            team2.tf_team_matches_played += 1

            team1_player1.tf_matches_played += 1
            team1_player2.tf_matches_played += 1
            team2_player1.tf_matches_played += 1
            team2_player2.tf_matches_played += 1

            if team1_score > team2_score:
                team1_player1.tf_matches_won += 1
                team1_player2.tf_matches_won += 1
                team1.tf_team_matches_won += 1
            else:
                team2_player1.tf_matches_won += 1
                team2_player2.tf_matches_won += 1
                team2.tf_team_matches_won += 1

            team1_player1.save()
            team1_player2.save()
            team2_player1.save()
            team2_player2.save()

            team1.save()
            team2.save()

            match.update_elos()

            return redirect('tf_games')

    else:
        match_form = TfNewMatchForm()

    return render(request, "tf/enter_tf_match.html", {'tf_match_form' : match_form})

def enter_fifa_match(request):
    if request.method == "POST":
        match_form = FifaNewMatchForm(request.POST, request=request)
        if match_form.is_valid():
            team1_player1 = match_form.cleaned_data['team1_player1']
            team1_player2 = match_form.cleaned_data['team1_player2']
            team1_score = match_form.cleaned_data['team1_score']

            team2_player1 = match_form.cleaned_data['team2_player1']
            team2_player2 = match_form.cleaned_data['team2_player2']
            team2_score = match_form.cleaned_data['team2_score']

            team1 = get_team(team1_player1, team1_player2)
            team2 = get_team(team2_player1, team2_player2)

            if team1.id < team2.id:
                scores = str(team1_score) + ' ' + str(team2_score)
            else:
                scores = str(team2_score) + ' ' + str(team1_score)

            match = FifaMatch(scores=scores, played_date=timezone.now())
            match.save()
            match.teams.add(team1, team2)
            match.save()

            team1.fifa_team_matches_played += 1
            team2.fifa_team_matches_played += 1

            team1_player1.fifa_matches_played += 1
            team1_player2.fifa_matches_played += 1
            team2_player1.fifa_matches_played += 1
            team2_player2.fifa_matches_played += 1

            if team1_score > team2_score:
                team1_player1.fifa_matches_won += 1
                team1_player2.fifa_matches_won += 1
                team1.fifa_team_matches_won += 1
            else:
                team2_player1.fifa_matches_won += 1
                team2_player2.fifa_matches_won += 1
                team2.fifa_team_matches_won += 1

            team1_player1.save()
            team1_player2.save()
            team2_player1.save()
            team2_player2.save()

            team1.save()
            team2.save()

            match.update_elos()

            return redirect('fifa_games')

    else:
        match_form = FifaNewMatchForm()

    return render(request, "tf/enter_fifa_match.html", {'fifa_match_form' : match_form})
