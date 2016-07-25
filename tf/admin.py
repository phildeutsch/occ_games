from django.contrib import admin

# Register your models here.
from .models import Player, Team, TfMatch, FifaMatch

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(TfMatch)
admin.site.register(FifaMatch)
