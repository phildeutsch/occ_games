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
    tf_players_ordered = Player.objects.all().filter(id__gt=0).filter(tf_matches_played__gt=0).order_by('-tf_player_elo')[:config.LEAGUE_LENGTH]
    fifa_players_ordered = Player.objects.all().filter(id__gt=0).filter(fifa_matches_played__gt=0).order_by('-fifa_player_elo')[:config.LEAGUE_LENGTH]

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

def games(request):
    if request.user.is_superuser:
        tf_matches = TfMatch.objects.order_by('-played_date').all()
        fifa_matches = FifaMatch.objects.order_by('-played_date').all()
    else:
        player = request.user.player
        tf_matches = [x.tfmatch_set.all() for x in player.team_set.all()]
        tf_matches = [item for sublist in tf_matches for item in sublist]
        tf_matches = sorted(tf_matches, key=lambda x:x.played_date, reverse=True)

        fifa_matches = [x.fifamatch_set.all() for x in player.team_set.all()]
        fifa_matches = [item for sublist in fifa_matches for item in sublist]
        fifa_matches = sorted(fifa_matches, key=lambda x:x.played_date, reverse=True)

    return render(request, "tf/games.html", {'tf_matches' : tf_matches, 'fifa_matches' : fifa_matches})

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

            return redirect('home')

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

            return redirect('home')

    else:
        match_form = FifaNewMatchForm()

    return render(request, "tf/enter_fifa_match.html", {'fifa_match_form' : match_form})
