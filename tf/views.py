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
