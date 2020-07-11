from unittest import TestCase
from player import Player


class TestPlayer(TestCase):
    def setUp(self):
        self._player = Player({}, None, {})
