from unittest import TestCase
from unittest.mock import Mock
from main import Application
from newgamepanel import NewGamePanel
from newplayerfield import NewPlayerField


class TestNewPlayerField(TestCase):

    @classmethod
    def setUpClass(cls):
        # TODO The following lines should not be here in a proper unit test case
        cls.application = Application()
        cls.application.set_new_language("en")

    def setUp(self):
        NewPlayerField._render_blank_image = Mock()
        # TODO The following line should not be here in a proper unit test case
        new_game_panel = NewGamePanel(self.application)
        self._new_player_field = NewPlayerField(new_game_panel)
        self._dummy_color = "#123456"

    def test_get_player_state(self):
        self._new_player_field.empire_picker.get = Mock(return_value="Pirate")
        self._new_player_field.picked_color.set("#000000")
        result = self._new_player_field.get_player_state()
        self.assertEqual("", result.name)
        self.assertEqual("#000000", result.color)
        self.assertEqual("Pirate", result.empire)

    def test_set_player_state(self):
        state = Mock()
        state.color = self._dummy_color
        state.name = "Roger"
        state.empire = "Pirate"
        self._new_player_field.set_player_state(state)
        self.assertEqual(1, self._new_player_field.active.get())
        self.assertEqual("Roger", self._new_player_field.name.get())
        self.assertEqual(self._dummy_color, self._new_player_field.picked_color.get())
        self.assertEqual(self._dummy_color, self._new_player_field._color.cget("bg"))
        self.assertEqual("Pirate", self._new_player_field.empire_picker.get())

    def test_set_player_state_blank(self):
        state = Mock()
        state.color = ""
        state.name = ""
        state.empire = ""
        self._new_player_field.set_player_state(state)
        self.assertEqual(1, self._new_player_field.active.get())
        self.assertEqual("", self._new_player_field.name.get())
        self.assertEqual("", self._new_player_field.picked_color.get())
        self.assertEqual("", self._new_player_field.empire_picker.get())
