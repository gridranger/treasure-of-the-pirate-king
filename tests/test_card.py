from unittest import TestCase
from unittest.mock import patch
from assets.cards.card import EventCard, LootCard
from assets.cards.eventcardtypes import EventCardTypes


class TestCardClasses(TestCase):

    @patch("settings.ApplicationSettings.language.get", side_effect=["title", "text"])
    @patch("settings.ApplicationSettings.language")
    def test_card(self, language, get):
        card = EventCard(EventCardTypes.bobbydick)
        self.assertEqual("title", card.title)
        self.assertEqual("text", card.text)
        self.assertEqual("bobbydick", card.id)
        self.assertTrue(repr(card).startswith("EventCard object at "))

    @patch("settings.ApplicationSettings.language.get", return_value="{} gold")
    @patch("settings.ApplicationSettings.language")
    def test_treasure_card(self, language, get):
        card = LootCard(50)
        card1 = LootCard(51)
        self.assertEqual("50 gold", card.text)
        self.assertTrue(repr(card).startswith("LootCard object, value 50, id treasure_"))
        self.assertEqual(card._loot_id + 1, card1._loot_id)
