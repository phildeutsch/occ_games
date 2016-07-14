from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', logout, {'next_page': '/tf'}),
    url(r'^new_player/$', views.player_new, name='player_new'),
    url(r'^team_league/$', views.team_league, name='team_league'),
    url(r'^player_league/$', views.player_league, name='player_league'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^rules/$', views.rules, name='rules'),
    url(r'^register/$', views.register, name='register'),
    url(r'^games/$', views.games, name='games'),
]
