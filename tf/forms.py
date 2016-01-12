from django import forms

from .models import TfPlayer


class TfNewPlayerForm(forms.ModelForm):
    class Meta:
        model = TfPlayer
        fields = ('first_name', 'last_name',)

class TfNewMatchForm(forms.Form):
    players = TfPlayer.objects.order_by('last_name')

    team1_player1 = forms.ModelChoiceField(queryset=players, label='Team 1, Player 1', initial=0)
    team1_player2 = forms.ModelChoiceField(queryset=players, label='Team 1, Player 2', initial=0)
    team1_score = forms.IntegerField(initial=0)

    team2_player1 = forms.ModelChoiceField(queryset=players, label='Team 2, Player 1', initial=0)
    team2_player2 = forms.ModelChoiceField(queryset=players, label='Team 2, Player 2', initial=0)
    team2_score = forms.IntegerField(initial=0)

    # def is_valid(self):
    #     player_list = [self.team1_player1, self.team1_player2, self.team2_player1, self.team2_player2]
    #
    #     return len(player_list) == len(set(player_list))

# TODO: Validation
# each player can only be once involved
# each team has to have at least one player
# one score has to be greater than 0
# score needs to be different (there needs to ba winner)

# update game counter after each match
