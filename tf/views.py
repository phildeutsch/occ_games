from django.shortcuts import render
from django.shortcuts import redirect
from .models import TfMatch
from .forms import TfPlayerForm

# Create your views here.
def index(request):
    matches = TfMatch.objects.order_by('played_date')[:5]
    return render(request, "tf/index.html", {'matches': matches})

def player_new(request):
    if request.method == "POST":
        new_player_form = TfPlayerForm(request.POST)
        if new_player_form.is_valid():
            player = new_player_form.save(commit=False)
            player.save()
            return redirect('index')
    else:
        new_player_form = TfPlayerForm()
    return render(request, 'tf/add_player.html', {'form': new_player_form})
