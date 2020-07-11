from unittest import TestCase
from savehandler import SaveHandler


class TestSaveHandler(TestCase):
    def setUp(self):
        self._save_handler = SaveHandler(None)
