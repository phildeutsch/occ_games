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
            p.tf_matches_played = 0
            p.tf_matches_won = 0
            p.fifa_matches_played = 0
            p.fifa_matches_won = 0
            p.save()

        # Go through all TF  matches and updated elOs
        print("Updating all TF ELOs")
        matches = models.TfMatch.objects.filter(season=config.SEASON).order_by('played_date').all()
        for m in matches:
            m.update_elos(debug=True)
            players = [x.players.all() for x in m.teams.all()]
            players = [item for sublist in players for item in sublist]
            for p in players:
                p.tf_last_played = m.played_date
                p.save()

        # Go through all FIFA matches and updated elOs
        print("Updating all FIFA ELOs")
        matches = models.FifaMatch.objects.filter(season=config.SEASON).order_by('played_date').all()
        for m in matches:
            m.update_elos(debug=True)
            players = [x.players.all() for x in m.teams.all()]
            players = [item for sublist in players for item in sublist]
            for p in players:
                p.tf_last_played = m.played_date
                p.save()
