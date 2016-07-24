# exec(open("fix_everything.py").read(), globals())

import config
from tf import models

# Set default ELO for each player
players = models.Player.objects.all()
for p in players:
    p.tf_player_elo = config.DEFAULT_ELO
    p.fifa_player_elo = config.DEFAULT_ELO
    p.save()

# Go through all TF  matches and updated elOs
matches = models.TfMatch.objects.order_by('played_date').all()
for m in matches:
    m.update_elos(debug=True)
    players = [x.players.all() for x in m.teams.all()]
    players = [item for sublist in players for item in sublist]
    for p in players:
        p.tf_last_played = m.played_date
        p.save()

# Go through all FIFA matches and updated elOs
matches = models.FifaMatch.objects.order_by('played_date').all()
for m in matches:
    m.update_elos(debug=True)
    players = [x.players.all() for x in m.teams.all()]
    players = [item for sublist in players for item in sublist]
    for p in players:
        p.tf_last_played = m.played_date
        p.save()
