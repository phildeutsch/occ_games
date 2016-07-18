from django import forms
from django.core.exceptions import ValidationError
from .models import TfPlayer
from django.contrib.auth.models import User
import re

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        form_data = self.cleaned_data
        try:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']

            if username == '':
                self.add_error(None, ValidationError("Please enter a username"))

            if username in [u.username for u in User.objects.all()]:
                raise forms.ValidationError(u'Username "%s" is already in use.' % username)

            if re.search(r'@occstrategy.com$', username) is None:
                raise forms.ValidationError(u'Please use an OC&C email address')

        except KeyError:
            self.add_error(None, ValidationError("Please enter all information"))

        return form_data

class TfNewPlayerForm(forms.ModelForm):
    class Meta:
        model = TfPlayer
        fields = ('first_name', 'last_name',)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name.strip()
        first_name = first_name.capitalize()

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name.strip()
        last_name = last_name.capitalize()

        return last_name

    def clean(self):
        form_data = self.cleaned_data
        try:
            first_name = form_data['first_name']
            last_name = form_data['last_name']
        except KeyError:
            first_name = ''
            last_name = ''
            self.add_error(None, ValidationError("Please enter a first and last name"))

        full_name = first_name + ' ' + last_name
        if TfPlayer.objects.all().filter(full_name__exact=full_name).exists():
            self.add_error(None, ValidationError("This player is already in the database"))

        return form_data


class TfNewMatchForm(forms.Form):
    players = TfPlayer.objects.order_by('last_name')

    team1_player1 = forms.ModelChoiceField(queryset=players, label='Player 1', initial=0)
    team1_player2 = forms.ModelChoiceField(queryset=players, label='Player 2', initial=0)
    team1_score = forms.IntegerField(initial=0, label='Score')

    team2_player1 = forms.ModelChoiceField(queryset=players, label='Player 1', initial=0)
    team2_player2 = forms.ModelChoiceField(queryset=players, label='Player 2', initial=0)
    team2_score = forms.IntegerField(initial=0, label='Score')

    invisible = forms.BooleanField(label='Hide from recent matches', initial=False, required=False)

    def clean(self):
        form_data = self.cleaned_data
        team1_player1 = form_data['team1_player1']
        team1_player2 = form_data['team1_player2']
        team1_score = form_data['team1_score']

        team2_player1 = form_data['team2_player1']
        team2_player2 = form_data['team2_player2']
        team2_score = form_data['team2_score']

        invisible = form_data['invisible']

        player_list = list(filter(lambda x: x.id > 0, [team1_player1, team1_player2, team2_player1, team2_player2]))

        if len(list(player_list)) != len(set(player_list)):
            self.add_error(None, ValidationError("Each player can only play once"))

        if team1_score == 0 and team2_score == 0:
            self.add_error(None, ValidationError("Must play at least one game"))

        if team1_score < 0 or team2_score < 0:
            self.add_error(None, ValidationError("Cannot play a negative number of games!"))

        if (team1_player1.id == 0 and team1_player2.id == 0) or \
                (team2_player1.id == 0 and team2_player2.id == 0):
            self.add_error(None, ValidationError("Each team must have at least one player"))

        return form_data
