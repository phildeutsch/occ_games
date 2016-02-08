from __future__ import unicode_literals

from django.db import models
import os

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
    player_elo = models.IntegerField(default=800)
    matches_played = models.IntegerField(default=0)

    # def __eq__(self, other):
    #     return self.first_name == other.first_name and self.last_name == other.last_name

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name

class TfTeam(models.Model):
    player1 = models.ForeignKey(TfPlayer, related_name='player1')
    player2 = models.ForeignKey(TfPlayer, related_name='player2')
    team_elo = models.IntegerField(default=0)
    team_matches_played = models.IntegerField(default=0)
    is_single_player = models.BooleanField(default=False)

    def update_elo(self):
        if self.is_single_player:
            self.team_elo = self.player2.player_elo
        else:
            self.team_elo = (self.player1.player_elo + self.player2.player_elo) / 2
        self.save()

    def __str__(self):
        if self.is_single_player:
            return str(self.player2)
        else:
            return str(self.player1) + os.linesep + str(self.player2)

class TfMatch(models.Model):
    team1 = models.ForeignKey(TfTeam, related_name='team1')
    team2 = models.ForeignKey(TfTeam, related_name='team2')
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    played_date = models.DateTimeField('date played')

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

    def update_player_elos(self):
        elo_change(self.team1.player1, self.team2.team_elo, self.score1, self.score2)
        elo_change(self.team1.player2, self.team2.team_elo, self.score1, self.score2)
        elo_change(self.team2.player1, self.team1.team_elo, self.score2, self.score1)
        elo_change(self.team2.player2, self.team1.team_elo, self.score2, self.score1)

    def __str__(self):
        if self.score1 > self.score2:
            return  str(self.team1) + ' ' + str(self.score1) + '-' \
               + str(self.score2) + ' ' + str(self.team2)
        else:
            return  str(self.team2) + ' ' + str(self.score2) + '-' \
               + str(self.score1) + ' ' + str(self.team1)
