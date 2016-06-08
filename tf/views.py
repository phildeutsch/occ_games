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

def home(request):
    matches = TfMatch.objects.order_by('-played_date')[:3]
    players_ordered = TfPlayer.objects.all().filter(id__gt=0).order_by('-player_elo')
    modal_js = ''

    if request.method == 'POST':

        if 'add_player-first_name' in request.POST:
            match_form = TfNewMatchForm(prefix='add_match')
            player_form = TfNewPlayerForm(request.POST, prefix='add_player')
            if player_form.is_valid():
                player = player_form.save(commit=False)
                player.full_name = player.first_name + ' ' + player.last_name
                player.save()
                return redirect('home')
            else:
                modal_js='<script type=\"text/javascript\">' \
                         '$(window).load(function(){' \
                         '$(\'#enter_player_dialog\').modal(\'show\');' \
                         '});</script>'

        elif 'add_match-team1_score' in request.POST:
            player_form = TfNewPlayerForm(prefix='add_player')
            match_form = TfNewMatchForm(request.POST, prefix='add_match')
            if match_form.is_valid():
                team1_player1 = match_form.cleaned_data['team1_player1']
                team1_player2 = match_form.cleaned_data['team1_player2']
                team1_score = match_form.cleaned_data['team1_score']

                team2_player1 = match_form.cleaned_data['team2_player1']
                team2_player2 = match_form.cleaned_data['team2_player2']
                team2_score = match_form.cleaned_data['team2_score']

                team1 = get_team(team1_player1, team1_player2)
                team2 = get_team(team2_player1, team2_player2)

                match = TfMatch(team1=team1, team2=team2, score1=team1_score, score2=team2_score,
                                played_date=timezone.now())
                match.save()

                match.update_player_elos()
                team1.update_elo()
                team2.update_elo()

                team1.team_matches_played += 1
                team2.team_matches_played += 1

                team1_player1.matches_played += 1
                team1_player2.matches_played += 1
                team2_player1.matches_played += 1
                team2_player2.matches_played += 1

                if team1_score > team2_score:
                    team1_player1.matches_won += 1
                    team1_player2.matches_won += 1
                    team1.team_matches_won += 1
                else:
                    team2_player1.matches_won += 1
                    team2_player2.matches_won += 1
                    team2.team_matches_won += 1

                team1_player1.save()
                team1_player2.save()
                team2_player1.save()
                team2_player2.save()

                team1.save()
                team2.save()

                return redirect('home')
            else:
                modal_js='<script type=\"text/javascript\">' \
                         '$(window).load(function(){' \
                         '$(\'#enter_match_dialog\').modal(\'show\');' \
                         '});</script>'
    else:
        match_form = TfNewMatchForm(prefix='add_match')
        player_form = TfNewPlayerForm(prefix='add_player')

    return render(request, "tf/home.html", {'matches'      : matches,
                                             'players'      : players_ordered,
                                             'match_form'   : match_form,
                                             'player_form'  : player_form,
                                             'modal_js'     : modal_js})


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
    teams_ordered = TfTeam.objects.all().filter(is_single_player__exact=False).order_by('-team_elo')

    return render(request, "tf/team_league.html", {'teams'        : teams_ordered})

def player_league(request):
    players_ordered = TfPlayer.objects.all().filter(id__gt=0).order_by('-player_elo')

    return render(request, "tf/player_league.html", {'players'        : players_ordered})

def faq(request):
    return render(request, "tf/faq.html",{})

def rules(request):
    return render(request, "tf/rules.html",{})
