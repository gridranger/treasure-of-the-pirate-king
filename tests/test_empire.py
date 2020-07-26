from unittest import TestCase
from assets import Empires


class TestEmpire(TestCase):
    def test_get_empire_by_name(self):
        for empire in Empires:
            empire.value.name = empire.value.adjective
        self.assertEqual(Empires.PIRATE.value, Empires.get_by_name("Pirate"))

    def test_get_empire_by_name_fail(self):
        with self.assertRaises(RuntimeError, msg="Invalid empire name: 'Portugal'"):
            self.assertEqual(Empires.PIRATE.value, Empires.get_by_name("Portugal"))

    def test_get_empire_by_adjective(self):
        self.assertEqual(Empires.PIRATE.value, Empires.get_by_adjective("Pirate"))

    def test_get_empire_by_adjective_fail(self):
        with self.assertRaises(RuntimeError, msg="Invalid empire name: 'Portugal'"):
            self.assertEqual(Empires.PIRATE.value, Empires.get_by_adjective("Portugal"))

    def test_get_names(self):
        self.assertEqual(['British', 'French', 'Dutch', 'Spanish', 'Pirate'], Empires.get_names())
