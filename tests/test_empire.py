from unittest import TestCase
from assets import Empire


class TestEmpire(TestCase):
    def test_get_empire_by_name(self):
        for empire in Empire:
            empire.value.name = empire.value.adjective
        self.assertEqual(Empire.PIRATE.value, Empire.get_by_name("Pirate"))

    def test_get_empire_by_name_fail(self):
        with self.assertRaises(RuntimeError, msg="Invalid empire name: 'Portugal'"):
            self.assertEqual(Empire.PIRATE.value, Empire.get_by_name("Portugal"))

    def test_get_empire_by_id(self):
        self.assertEqual(Empire.PIRATE.value, Empire.get_by_id("Pirate"))

    def test_get_empire_by_id_fail(self):
        with self.assertRaises(RuntimeError, msg="Invalid empire name: 'Portugal'"):
            self.assertEqual(Empire.PIRATE.value, Empire.get_by_id("Portugal"))

    def test_get_names(self):
        self.assertEqual(['British', 'French', 'Dutch', 'Spanish', 'Pirate'], Empire.get_names())
