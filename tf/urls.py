from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^new_player/$', views.player_new, name='player_new'),
    url(r'^player_league/$', views.player_league, name='player_league'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^rules/$', views.rules, name='rules'),
    url(r'^register/$', views.register, name='register'),
    url(r'^games/$', views.games, name='games'),
    url(r'^enter_tf_match/$', views.enter_tf_match, name='enter_tf_match'),
    url(r'^enter_player/$', views.enter_player, name='enter_tf_match'),

    url(r'^accounts/',
        include('registration.backends.default.urls')),
    url(r'^accounts/profile/',
        TemplateView.as_view(template_name='profile.html'),
        name='profile'),
    url(r'^login/',
        auth_views.login,
        name='login'),
    url(r'^admin/',
        include(admin.site.urls),
        name='admin'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/tf'}),

]
