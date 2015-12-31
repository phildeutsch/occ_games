from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TfPlayer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    grade = models.CharField(max_length=2, default='AC')
    score = models.IntegerField(default=800)
    matches_played = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class TfTeam(models.Model):
    player1 = models.ForeignKey(TfPlayer, related_name='player1')
    player2 = models.ForeignKey(TfPlayer, related_name='player2')
    team_matches_played = models.IntegerField(default=0)

    def __str__(self):
        return str(self.player1) + ', ' + str(self.player2)

class TfMatch(models.Model):
    team1 = models.ForeignKey(TfTeam, related_name='team1')
    team2 = models.ForeignKey(TfTeam, related_name='team2')
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    played_date = models.DateTimeField('date played')

    def __str__(self):
        return 'Match ' + str(self.id) + ': ' \
               + str(self.team1) + ' ' + str(self.score1) + '-' \
               + str(self.score2) + ' ' + str(self.team2)
