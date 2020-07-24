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
