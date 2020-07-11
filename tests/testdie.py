from random import randint
from unittest import TestCase
from unittest.mock import patch
from assets import Die


class TestDie(TestCase):

    def setUp(self):
        self._color_hex = "#80eb56"
        self._die = Die(None, 60, self._color_hex, "black", 1)

    @patch("die.Die._show")
    @patch("die.Die._show_dots")
    def test___init__(self, _show_dots, _show):
        self._die = Die(None, 60, "#80eb56", "black", 1)
        self.assertEqual(30, self._die._y)
        self.assertEqual(6, self._die._dot_radius)
        _show.assert_called()
        _show_dots.assert_called()

    @patch("tkinter.Canvas.create_rectangle")
    def test__show(self, create_rectangle):
        self._die._show()
        create_rectangle.assert_called_once_with(2, 2, 62, 62, fill=self._color_hex, width=0)

    @patch("tkinter.Canvas.create_oval")
    def test__show_dots(self, create_oval):
        test_value = randint(1, 6)
        self._die._current_value = test_value
        self._die._dot_list = []
        self._die._show_dots()
        self.assertEqual(test_value, create_oval.call_count)
        self.assertEqual(test_value, len(self._die._dot_list))

    @patch("tkinter.Canvas.create_oval")
    def test__show_dots_call_values(self, create_oval):
        self._die._show_dots()
        create_oval.assert_called_with(26, 26, 38, 38, fill="black")

    @patch("tkinter.Canvas.delete")
    def test__remove_dots(self, delete):
        test_value = randint(1, 6)
        self._die._current_value = test_value
        self._die._dot_list = []
        self._die._show_dots()
        self._die._remove_dots()
        self.assertEqual(test_value, delete.call_count)

    @patch("die.Die._remove_dots")
    @patch("die.Die._show_dots")
    @patch("tkinter.Canvas.update_idletasks")
    def test_roll(self, update_idletasks, _show_dots, _remove_dots):
        self.assertTrue(self._die.roll() in range(1,7))
        self.assertEqual(6, _remove_dots.call_count)
        self.assertEqual(6, _show_dots.call_count)
        self.assertEqual(6, update_idletasks.call_count)
