from unittest import TestCase
from main import Application


class TestApplication(TestCase):
    def setUp(self):
        self._application = Application()
