from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import TfMatch, Player, TfTeam
from .forms import TfNewPlayerForm, TfNewMatchForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import config
import re

# TODO move to central functions file
def get_team(player1, player2):
    if player1.id > player2.id:
        tmp = player1
        player1 = player2
        player2 = tmp
    try:
        team = TfTeam.objects.filter(players=player1).filter(players=player2)[0]
    except IndexError:
        team = TfTeam()
        team.save()
        if player1.id != 0:
            team.players.add(player1)
        if player2.id != 0:
            team.players.add(player2)
        team.is_single_player = True if len(team.players.all())==1 else False
        team.save()
    return team

def home(request):
    matches = TfMatch.objects.order_by('-played_date').filter(invisible=False)[:config.RECENT_MATCHES]
    players_ordered = Player.objects.all().filter(id__gt=0).order_by('-tf_player_elo')[:config.LEAGUE_LENGTH]
    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = 'Log In'

    match_form = TfNewMatchForm(prefix='add_match')
    player_form = TfNewPlayerForm(prefix='add_player')

    return render(request, "tf/home.html", {'user'         : request.user,
                                            'matches'      : matches,
                                            'players'      : players_ordered})

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

def team_league(request):
    teams_ordered = sorted(TfTeam.objects.all().filter(is_single_player__exact=False), key=lambda x:-x.team_elo())[:config.LEAGUE_LENGTH]

    return render(request, "tf/team_league.html", {'teams'        : teams_ordered})

def player_league(request):
    players_ordered = Player.objects.all().filter(id__gt=0).order_by('-tf_player_elo')[:config.LEAGUE_LENGTH]

    return render(request, "tf/player_league.html", {'players'        : players_ordered})

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
    # matches_ordered = TfMatch.objects.order_by('-played_date').all()
    player = request.user.player
    matches = [x.tfmatch_set.all() for x in player.tfteam_set.all()]
    matches = [item for sublist in matches for item in sublist]
    matches = sorted(matches, key=lambda x:x.played_date, reverse=True)

    return render(request, "tf/games.html", {'matches' : matches})

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

            invisible = match_form.cleaned_data['invisible']

            if team1.id < team2.id:
                scores = str(team1_score) + ' ' + str(team2_score)
            else:
                scores = str(team2_score) + ' ' + str(team1_score)

            match = TfMatch(scores=scores,
                            played_date=timezone.now(), invisible=invisible)
            match.save()
            match.teams.add(team1, team2)
            match.save()

            team1.team_matches_played += 1
            team2.team_matches_played += 1

            team1_player1.tf_matches_played += 1
            team1_player2.tf_matches_played += 1
            team2_player1.tf_matches_played += 1
            team2_player2.tf_matches_played += 1

            if team1_score > team2_score:
                team1_player1.tf_matches_won += 1
                team1_player2.tf_matches_won += 1
                team1.team_matches_won += 1
            else:
                team2_player1.tf_matches_won += 1
                team2_player2.tf_matches_won += 1
                team2.team_matches_won += 1

            team1_player1.save()
            team1_player2.save()
            team2_player1.save()
            team2_player2.save()

            team1.save()
            team2.save()

            match.update_elos()

            return redirect('home')

    else:
        match_form = match_form = TfNewMatchForm()

    return render(request, "tf/enter_tf_match.html", {'match_form' : match_form})
