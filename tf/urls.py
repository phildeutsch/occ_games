from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^new_player/$', views.player_new, name='player_new'),
    url(r'^team_league/$', views.team_league, name='team_league'),
    url(r'^player_league/$', views.player_league, name='player_league'),
]
