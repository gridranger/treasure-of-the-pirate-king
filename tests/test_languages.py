from unittest import TestCase
from localization import Languages
from localization.localization import Localization


class TestLanguages(TestCase):
    def test_get_language_by_name(self):
        self.assertEqual(Languages.HUNGARIAN.value, Languages.get_language_by_name("Magyar"))

    def test_get_language_by_name_non_existing_language(self):
        with self.assertRaises(RuntimeError, msg="No such language as 'Quenya'. Available languages are: Magyar, "
                                                 "Kalóz, English."):
            Languages.get_language_by_name("Quenya")

    def test__fetch_term_non_existing(self):
        with self.assertRaises(NotImplementedError, msg="Translataion of term 'this_language' is missing from the  "
                                                        "language."):
            Localization()
