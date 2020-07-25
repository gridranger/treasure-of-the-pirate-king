from unittest import TestCase
from settings import ApplicationSettings


class TestSettings(TestCase):
    def test_tile_size(self):
        self.assertEqual(85, ApplicationSettings.tile_size)
