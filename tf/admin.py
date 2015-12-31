from django.contrib import admin

# Register your models here.
from .models import TfPlayer, TfTeam, TfMatch

admin.site.register(TfPlayer)
admin.site.register(TfTeam)
admin.site.register(TfMatch)