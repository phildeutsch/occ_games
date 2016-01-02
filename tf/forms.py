from django import forms

from .models import TfPlayer


class TfNewPlayerForm(forms.ModelForm):
    class Meta:
        model = TfPlayer
        fields = ('first_name', 'last_name',)

class TfNewMatchForm(forms.Form):
    players = TfPlayer.objects.order_by('last_name')

    team1_player1 = forms.ModelChoiceField(queryset=players, label='Team 1, Player 1', empty_label="No Player")
    team1_player2 = forms.ModelChoiceField(queryset=players, label='Team 1, Player 2', empty_label="No Player")
    team1_score = forms.IntegerField()

    team2_player1 = forms.ModelChoiceField(queryset=players, label='Team 2, Player 1', empty_label="No Player")
    team2_player2 = forms.ModelChoiceField(queryset=players, label='Team 2, Player 2', empty_label="No Player")
    team2_score = forms.IntegerField()

    # def is_valid(self):
    #     player_list = [self.team1_player1, self.team1_player2, self.team2_player1, self.team2_player2]
    #
    #     return len(player_list) == len(set(player_list))
