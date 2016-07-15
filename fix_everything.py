# exec(open("recalculate_elos.py").read(), globals())

import config
from tf import models

# Set default ELO for each player
players = models.TfPlayer.objects.all()
for p in players:
    p.player_elo = config.DEFAULT_ELO
    p.save()

# Go through all matches and updated elOs
matches = models.TfMatch.objects.order_by('played_date').all()
for m in matches:
    m.update_elos(debug=False)

# Make sure each user has a player linked to them
