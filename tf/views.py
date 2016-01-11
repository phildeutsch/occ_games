from django.shortcuts import render, redirect
from django.utils import timezone
from .models import TfMatch, TfPlayer, TfTeam
from .forms import TfNewPlayerForm, TfNewMatchForm

# TODO move to central functions file
def get_team(player1, player2):
    if player1.id > player2.id:
        tmp = player1
        player1 = player2
        player2 = tmp

    try:
        team = TfTeam.objects.get(player1=player1, player2=player2)
    except TfTeam.DoesNotExist:
        team = TfTeam(player1=player1, player2=player2, team_matches_played=0)
        team.is_single_player = True if player1.id == 0 else False
        team.update_elo()
        team.save()

    return team

# Create your views here.
def index(request):
    matches = TfMatch.objects.order_by('-played_date')[:5]
    players = TfPlayer.objects.order_by('-player_elo')

    if request.method == 'POST':
        match_form = TfNewMatchForm(request.POST)
        if match_form.is_valid():
            team1_player1 = match_form.cleaned_data['team1_player1']
            team1_player2 = match_form.cleaned_data['team1_player2']
            team1_score = match_form.cleaned_data['team1_score']

            team2_player1 = match_form.cleaned_data['team2_player1']
            team2_player2 = match_form.cleaned_data['team2_player2']
            team2_score = match_form.cleaned_data['team2_score']

            team1 = get_team(team1_player1, team1_player2)
            team2 = get_team(team2_player1, team2_player2)

            match = TfMatch(team1=team1, team2=team2, score1=team1_score, score2=team2_score, played_date=timezone.now())
            match.save()

            match.update_player_elos()
            team1.update_elo()
            team2.update_elo()

            return redirect('index')

    else:
        match_form = TfNewMatchForm()

    return render(request, "tf/index.html", {'matches': matches,
                                             'players': players,
                                             'match_form': match_form})



def player_new(request):
    if request.method == "POST":
        new_player_form = TfNewPlayerForm(request.POST)
        if new_player_form.is_valid():
            player = new_player_form.save(commit=False)
            player.full_name = player.first_name + ' ' + player.last_name
            player.save()
            return redirect('index')
    else:
        new_player_form = TfNewPlayerForm()
    return render(request, 'tf/add_player.html', {'form': new_player_form})
