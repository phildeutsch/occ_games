from django import forms
from django.core.exceptions import ValidationError
from .models import TfPlayer


class TfNewPlayerForm(forms.ModelForm):
    class Meta:
        model = TfPlayer
        fields = ('first_name', 'last_name',)

class TfNewMatchForm(forms.Form):
    players = TfPlayer.objects.order_by('last_name')

    team1_player1 = forms.ModelChoiceField(queryset=players, label='Player 1', initial=0)
    team1_player2 = forms.ModelChoiceField(queryset=players, label='Player 2', initial=0)
    team1_score = forms.IntegerField(initial=0, label='Score')

    team2_player1 = forms.ModelChoiceField(queryset=players, label='Player 1', initial=0)
    team2_player2 = forms.ModelChoiceField(queryset=players, label='Player 2', initial=0)
    team2_score = forms.IntegerField(initial=0, label='Score')

    def clean(self):
        form_data = self.cleaned_data
        team1_player1 = form_data['team1_player1']
        team1_player2 = form_data['team1_player2']
        team1_score = form_data['team1_score']

        team2_player1 = form_data['team2_player1']
        team2_player2 = form_data['team2_player2']
        team2_score = form_data['team2_score']

        player_list = filter(lambda x: x.id > 0, [team1_player1, team1_player2, team2_player1, team2_player2])

        if len(list(player_list)) != len(set(player_list)):
            raise ValidationError("Each player can only play once")

        if team1_score == 0 and team2_score == 0:
            raise ValidationError("Must play at least one game")

        if (team1_player1.id == 0 and team1_player2.id == 0) or \
                (team2_player1.id == 0 and team2_player2.id == 0):
            raise ValidationError("Each team must have at least one player")

        return form_data

