from django.shortcuts import render
from django.http import HttpResponse
from .models import TfMatch
from .forms import TfPlayerForm

# Create your views here.
def index(request):
    matches = TfMatch.objects.order_by('played_date')[:5]
    new_player_form = TfPlayerForm()
    return render(request, "tf/index.html", {'matches': matches, 'form': new_player_form})
