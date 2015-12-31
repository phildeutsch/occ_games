from django.shortcuts import render
from django.shortcuts import redirect
from .models import TfMatch, TfPlayer
from .forms import TfNewPlayerForm

# Create your views here.
def index(request):
    matches = TfMatch.objects.order_by('played_date')[:5]
    players = TfPlayer.objects.order_by('-score')

    return render(request, "tf/index.html", {'matches': matches,
                                             'players': players})

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

def add_match(request):
    team1_player1_id = request.POST.get('team1_player1')
    team1_player2_id = request.POST.get('team1_player2')
    team2_player1_id = request.POST.get('team2_player1')
    team2_player2_id = request.POST.get('team2_player2')

    player_ids = [team1_player1_id, team1_player2_id, team2_player1_id, team2_player2_id]

    return redirect(index)
