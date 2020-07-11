from unittest import TestCase
from newgamepanel import NewGamePanel


class TestNewGamePanel(TestCase):
    def setUp(self):
        self._new_game_panel = NewGamePanel(None)
