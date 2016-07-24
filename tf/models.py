from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import os
import re
import config
import datetime

class Player(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    grade = models.CharField(max_length=2, default='AC')
    user = models.OneToOneField(User, null=True)

    # TF attributes
    tf_player_elo = models.IntegerField(default=config.DEFAULT_ELO)
    tf_matches_played = models.IntegerField(default=0)
    tf_matches_won = models.IntegerField(default=0)
    tf_last_played = models.DateTimeField(null=True)

    # FIFA attributes
    fifa_player_elo = models.IntegerField(default=config.DEFAULT_ELO)
    fifa_matches_played = models.IntegerField(default=0)
    fifa_matches_won = models.IntegerField(default=0)
    fifa_last_played = models.DateTimeField(null=True)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name

class Team(models.Model):
    players = models.ManyToManyField(Player)
    is_single_player = models.BooleanField(default=False)

    # TF attributes
    tf_team_matches_played = models.IntegerField(default=0)
    tf_team_matches_won = models.IntegerField(default=0)

    def tf_team_elo(self):
        if self.is_single_player:
            return int(self.players.order_by('id')[0].tf_player_elo)
        else:
            return int((self.players.order_by('id')[1].tf_player_elo + self.players.order_by('id')[0].tf_player_elo) / 2)

    def prettyprint(self):
        if self.is_single_player:
            s = str(self.players.order_by('id')[0])
        else:
            s = str(self.players.order_by('id')[0]) + ' / ' + str(self.players.order_by('id')[1])
        return s

    def __str__(self):
        s = ''
        for p in self.players.order_by('id'):
            s = s + str(p) + '\n'
        return s

class TfMatch(models.Model):
    class Meta:
        verbose_name_plural = "tf matches"

    teams = models.ManyToManyField(Team)
    scores = models.CharField(max_length=5, default="0 0")

    played_date = models.DateTimeField('date played')

    def scores_to_int(self):
        match = re.search('(.)\s(.)', self.scores)
        score1 = int(match.group(1))
        score2 = int(match.group(2))
        return [score1, score2]

    def get_winner(self):
        [score1, score2] = self.scores_to_int()
        teams = self.teams.order_by('id').all()

        if score1 > score2:
            return teams[0]
        else:
            return teams[1]

    def get_loser(self):
        [score1, score2] = self.scores_to_int()
        teams = self.teams.order_by('id').all()

        if score1 > score2:
            return teams[1]
        else:
            return teams[0]

    def get_scores(self):
        [score1, score2] = self.scores_to_int()

        if score1 > score2:
            return str(score1) + '-' + str(score2)
        else:
            return str(score2) + '-' + str(score1)

    def update_elos(self, k=32, debug=False):

        winner = self.get_winner()
        loser = self.get_loser()

        if debug:
            print(str(self.played_date)[:16])

            print("Before")
            print("W: ", end='')
            print(str(winner.players.order_by('id')[0]) + ' (' + str(winner.players.order_by('id')[0].tf_player_elo) + ')', end='')
            if not winner.is_single_player:
                print('/ ' + str(winner.players.order_by('id')[1]) + ' (' + str(winner.players.order_by('id')[1].tf_player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(winner.tf_team_elo())))

            print("L: ", end='')
            print(str(loser.players.order_by('id')[0]) + ' (' + str(loser.players.order_by('id')[0].tf_player_elo) + ')', end='')
            if not loser.is_single_player:
                print('/ ' + str(loser.players.order_by('id')[1]) + ' (' + str(loser.players.order_by('id')[1].tf_player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(loser.tf_team_elo())))

        elo_winner = winner.tf_team_elo()
        elo_loser = loser.tf_team_elo()

        e = 1 / (1 + 10 ** ((elo_loser-elo_winner)/400))
        delta_winner = k * (1 - e)
        delta_loser = k * (0 - e)

        for p in winner.players.all():
            p.tf_player_elo += delta_winner
            p.tf_last_played = datetime.datetime.now()
            p.save()

        for p in loser.players.all():
            p.tf_player_elo += delta_loser
            p.tf_last_played = datetime.datetime.now()
            p.save()

        if debug:
            print("After")
            print("W: ", end='')
            print(str(winner.players.order_by('id')[0]) + ' (' + str(winner.players.order_by('id')[0].tf_player_elo) + ')', end='')
            if not winner.is_single_player:
                print('/ ' + str(winner.players.order_by('id')[1]) + ' (' + str(winner.players.order_by('id')[1].tf_player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(winner.tf_team_elo())))

            print("L: ", end='')
            print(str(loser.players.order_by('id')[0]) + ' (' + str(loser.players.order_by('id')[0].tf_player_elo) + ')', end='')
            if not loser.is_single_player:
                print('/ ' + str(loser.players.order_by('id')[1]) + ' (' + str(loser.players.order_by('id')[0].tf_player_elo) + '): ', end='')
            else:
                print(': ', end='')
            print(str(round(loser.tf_team_elo())))

            print('---')

    def __str__(self):
        [score1, score2] = self.scores_to_int()

        if score1 > score2:
            return  str(self.get_winner()) + ' ' + str(score1) + '-' \
               + str(score2) + ' ' + str(self.get_loser())
        else:
            return  str(self.get_winner()) + ' ' + str(score2) + '-' \
               + str(score1) + ' ' + str(self.get_loser())

    def prettyprint(self):
        [score1, score2] = self.scores_to_int()

        if score1 > score2:
            return  self.get_winner().prettyprint() + ' ' + str(score1) + '-' \
               + str(score2) + ' ' + self.get_loser().prettyprint()
        else:
            return  self.get_winner().prettyprint() + ' ' + str(score2) + '-' \
               + str(score1) + ' ' + self.get_loser().prettyprint()
