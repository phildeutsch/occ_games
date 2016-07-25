from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import os
import re
import config

class Player(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    grade = models.CharField(max_length=2, default='AC')
    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return self.full_name

    def __unicode__(self):
        return self.full_name

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

class Team(models.Model):
    players = models.ManyToManyField(Player)
    is_single_player = models.BooleanField(default=False)

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

    # TF attributes & methods
    tf_team_matches_played = models.IntegerField(default=0)
    tf_team_matches_won = models.IntegerField(default=0)

    def tf_team_elo(self):
        if self.is_single_player:
            return int(self.players.order_by('id')[0].tf_player_elo)
        else:
            return int((self.players.order_by('id')[1].tf_player_elo + self.players.order_by('id')[0].tf_player_elo) / 2)

    # FIFA attributes & methods
    fifa_team_matches_played = models.IntegerField(default=0)
    fifa_team_matches_won = models.IntegerField(default=0)

    def fifa_team_elo(self):
        if self.is_single_player:
            return int(self.players.order_by('id')[0].fifa_player_elo)
        else:
            return int((self.players.order_by('id')[1].fifa_player_elo + self.players.order_by('id')[0].fifa_player_elo) / 2)

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

        team1 = self.teams.order_by('id').all()[0]
        team2 = self.teams.order_by('id').all()[1]

        elo1 = team1.tf_team_elo()
        elo2 = team2.tf_team_elo()

        score1 = self.scores_to_int()[0]
        score2 = self.scores_to_int()[1]

        R1 = 10 ** (elo1/400)
        R2 = 10 ** (elo2/400)

        E1 = R1 / (R1 + R2)
        E2 = R2 / (R1 + R2)

        if score1 > score2:
            S1 = 1
            S2 = 0
        elif score2 > score1:
            S1 = 0
            S2 = 1
        else:
            S1 = 0.5
            S2 = 0.5

        delta1 = k * (S1 - E1)
        delta2 = k * (S2 - E2)

        if debug:
            print("Team 1: " + str(elo1) + " " + str(score1) + " " + str(R1) + " " + str(E1) + " " + str(S1) + " " + str(elo1+delta1))
            print("Team 2: " + str(elo2) + " " + str(score2) + " " + str(R2) + " " + str(E2) + " " + str(S2) + " " + str(elo2+delta2))

        for p in team1.players.all():
            p.tf_player_elo += delta1
            p.tf_last_played = self.played_date
            p.save()

        for p in team2.players.all():
            p.tf_player_elo += delta2
            p.tf_last_played = self.played_date
            p.save()

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

class FifaMatch(models.Model):
    class Meta:
        verbose_name_plural = "fifa matches"

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

        team1 = self.teams.order_by('id').all()[0]
        team2 = self.teams.order_by('id').all()[1]

        elo1 = team1.fifa_team_elo()
        elo2 = team2.fifa_team_elo()

        score1 = self.scores_to_int()[0]
        score2 = self.scores_to_int()[1]

        R1 = 10 ** (elo1/400)
        R2 = 10 ** (elo2/400)

        E1 = R1 / (R1 + R2)
        E2 = R2 / (R1 + R2)

        if score1 > score2:
            S1 = 1
            S2 = 0
        elif score2 > score1:
            S1 = 0
            S2 = 1
        else:
            S1 = 0.5
            S2 = 0.5

        delta1 = k * (S1 - E1)
        delta2 = k * (S2 - E2)

        if debug:
            print("Team 1: " + str(elo1) + " " + str(score1) + " " + str(R1) + " " + str(E1) + " " + str(S1) + " " + str(elo1+delta1))
            print("Team 2: " + str(elo2) + " " + str(score2) + " " + str(R2) + " " + str(E2) + " " + str(S2) + " " + str(elo2+delta2))

        for p in team1.players.all():
            p.fifa_player_elo += delta1
            p.fifa_last_played = self.played_date
            p.save()

        for p in team2.players.all():
            p.fifa_player_elo += delta2
            p.fifa_last_played = self.played_date
            p.save()

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
