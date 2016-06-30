from tf import models
import config

players = models.TfPlayer.objects.all()
for p in players:
    p.player_elo = config.DEFAULT_ELO
    p.save()

matches = models.TfMatch.objects.order_by('played_date').all()
for m in matches:
    # update elos

teams = models.TfTeam.objects.all()
for t in teams:
    t.team_elo = config.DEFAULT_ELO
    t.save()
