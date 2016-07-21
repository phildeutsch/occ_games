from django.contrib import admin

# Register your models here.
from .models import Player, TfTeam, TfMatch

admin.site.register(Player)
admin.site.register(TfTeam)
admin.site.register(TfMatch)
