# exec(open("fix_everything.py").read(), globals())

import config
from tf import models
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, **options):
        # Go through all TF  matches and updated elOs
        print("Setting all ELOs to 1000")
        players = models.Player.objects.all()
        for p in players:
            p.tf_player_elo = config.DEFAULT_ELO
            p.fifa_player_elo = config.DEFAULT_ELO
            p.tf_last_played = None
            p.fifa_last_played = None
            p.save()
