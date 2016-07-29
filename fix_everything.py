# exec(open("fix_everything.py").read(), globals())

import config
from tf import models

def min_team_id(team):
    if team.is_single_player:
        sameteams = teams.filter(players=team.players.all()).filter(is_single_player=True)
    else:
        sameteams = teams.filter(players=team.players.all()[0]).filter(players=team.players.all()[1])
    min_team_id = min([t.id for t in sameteams])
    return min_team_id

def assign_min(m):
    team1 = m.teams.order_by('id').all()[0]
    team2 = m.teams.order_by('id').all()[1]

    score1 = m.scores_to_int()[0]
    score2 = m.scores_to_int()[1]

    m.teams.remove(team1, team2)

    new_id1 = min_team_id(team1)
    new_id2 = min_team_id(team2)

    m.teams.add(new_id1, new_id2)
    if new_id1 < new_id2:
        m.score = str(score1) + " " + str(score2)
    else:
        m.score = str(score2) + " " + str(score1)

# Assign the first team to each match before removing duplicate teams
print("Removing duplicate teams")
tf_matches = models.TfMatch.objects.all()
fifa_matches = models.FifaMatch.objects.all()
teams = models.Team.objects.all()
for m in tf_matches:
    print("TF game: " + str(m.id))
    assign_min(m)
for m in fifa_matches:
    print("FIFA game: " + str(m.id))
    assign_min(m)

players = models.Player.objects.filter(id__gt=0).all()
for player1 in players:
    print(player1)
    for player2 in players:
        if player1==player2:
            teams = models.Team.objects.filter(players=player1).filter(is_single_player=True).order_by('id').all()
        else:
            teams = models.Team.objects.filter(players=player1).filter(players=player2).order_by('id').all()

        if len(teams)>1:
            [t.delete() for t in teams[1:]]

print("Setting all ELOs to 1000")
players = models.Player.objects.all()
for p in players:
    p.tf_player_elo = config.DEFAULT_ELO
    p.fifa_player_elo = config.DEFAULT_ELO
    p.tf_last_played = None
    p.fifa_last_played = None
    p.save()

# Go through all TF  matches and updated elOs
print("Updating all TF ELOs")
matches = models.TfMatch.objects.order_by('played_date').all()
for m in matches:
    m.update_elos(debug=True)
    players = [x.players.all() for x in m.teams.all()]
    players = [item for sublist in players for item in sublist]
    for p in players:
        p.tf_last_played = m.played_date
        p.save()

# Go through all FIFA matches and updated elOs
print("Updating all FIFA ELOs")
matches = models.FifaMatch.objects.order_by('played_date').all()
for m in matches:
    m.update_elos(debug=True)
    players = [x.players.all() for x in m.teams.all()]
    players = [item for sublist in players for item in sublist]
    for p in players:
        p.tf_last_played = m.played_date
        p.save()
