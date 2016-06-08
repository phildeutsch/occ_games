from django.test import TestCase
from .models import TfMatch, TfPlayer, TfTeam
from .models import elo_change

# model tests
class EloChange(TestCase):

    p1 = TfPlayer(first_name='Test', last_name='Player 1')

    elo_change(p1, 1000, 3, 2, k=32)
