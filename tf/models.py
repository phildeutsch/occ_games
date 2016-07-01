from __future__ import unicode_literals

from django.db import models
import os
import config


# TODO Move this to separate functions file
def elo_change(player, elo2, score1, score2, k=32):
    s = 1 if score1 > score2 else 0 if score2 > score1 else 0.5
    e = 1 / (1 + 10 ** ((elo2-player.player_elo)/400))
    delta = k * (s - e)

    player.player_elo += delta
    player.save()

# Create your models here.
class TfPlayer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    grade = models.CharField(max_length=2, default='AC')
    player_elo = models.IntegerField(default=config.DEFAULT_ELO)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name

class TfTeam(models.Model):
    player1 = models.ForeignKey(TfPlayer, related_name='player1')
    player2 = models.ForeignKey(TfPlayer, related_name='player2')
    team_matches_played = models.IntegerField(default=0)
    team_matches_won = models.IntegerField(default=0)
    is_single_player = models.BooleanField(default=False)

    def team_elo(self):
        if self.is_single_player:
            return self.player2.player_elo
        else:
            return (self.player1.player_elo + self.player2.player_elo) / 2

    def __str__(self):
        if self.is_single_player:
            return str(self.player2)
        else:
            return str(self.player1) + os.linesep + str(self.player2)

class TfMatch(models.Model):
    class Meta:
        verbose_name_plural = "tf matches"

    team1 = models.ForeignKey(TfTeam, related_name='team1')
    team2 = models.ForeignKey(TfTeam, related_name='team2')
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    played_date = models.DateTimeField('date played')
    invisible = models.BooleanField(default=False)

    def get_winner(self):
        if self.score1 > self.score2:
            return self.team1
        else:
            return self.team2

    def get_loser(self):
        if self.score1 > self.score2:
            return self.team2
        else:
            return self.team1

    def get_scores(self):
        if self.score1 > self.score2:
            return str(self.score1) + '-' + str(self.score2)
        else:
            return str(self.score2) + '-' + str(self.score1)

    def update_elos(self, k=32, debug=False):

        print(self.played_date)

        winner = self.get_winner()
        loser = self.get_loser()

        if debug:
            print("winners:")
            print(str(winner.player2) + ' ' + str(winner.player2.player_elo))
            print(str(winner.player1) + ' ' + str(winner.player1.player_elo))
            print(str(winner.team_elo()))

            print("losers")
            print(str(loser.player2) + ' ' + str(loser.player2.player_elo))
            print(str(loser.player1) + ' ' + str(loser.player1.player_elo))
            print(str(loser.team_elo()))

        elo_winner = winner.team_elo()
        elo_loser = loser.team_elo()

        e = 1 / (1 + 10 ** ((elo_loser-elo_winner)/400))
        delta_winner = k * (1 - e)

        e = 1 / (1 + 10 ** ((elo_loser-elo_winner)/400))
        delta_loser = k * (0 - e)

        if debug:
            print("change winner")
            print(str(delta_winner))

            print("change loser")
            print(str(delta_loser))

        winner.player2.player_elo += delta_winner
        winner.player2.save()
        if not winner.is_single_player:
            winner.player1.player_elo += delta_winner
            winner.player1.save()

        loser.player2.player_elo += delta_loser
        loser.player2.save()
        if not loser.is_single_player:
            loser.player1.player_elo += delta_loser
            loser.player1.save()

        if debug:
            print("winners new:")
            print(str(winner.player2) + ' ' + str(winner.player2.player_elo))
            print(str(winner.player1) + ' ' + str(winner.player1.player_elo))
            print(str(winner.team_elo()))

            print("losers new")
            print(str(loser.player2) + ' ' + str(loser.player2.player_elo))
            print(str(loser.player1) + ' ' + str(loser.player1.player_elo))
            print(str(loser.team_elo()))

            print('---')

    def __str__(self):
        if self.score1 > self.score2:
            return  str(self.team1) + ' ' + str(self.score1) + '-' \
               + str(self.score2) + ' ' + str(self.team2)
        else:
            return  str(self.team2) + ' ' + str(self.score2) + '-' \
               + str(self.score1) + ' ' + str(self.team1)
