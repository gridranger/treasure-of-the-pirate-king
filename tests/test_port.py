from unittest import TestCase
from port import Varos


class TestPort(TestCase):
    def setUp(self):
        self._port = Varos(None, None, "dummy")
