from unittest import TestCase
from settings import Settings


class TestSettings(TestCase):
    def test_tile_size(self):
        self.assertEqual(85, Settings.tile_size)
