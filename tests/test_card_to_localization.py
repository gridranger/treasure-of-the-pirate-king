from unittest import TestCase
from assets.cards.card import EventCard, LootCard
from assets.cards.eventcardtypes import EventCardTypes
from settings import ApplicationSettings as s
from localization import Languages


class TestCardToLocalization(TestCase):
    def setUp(self):
        s.language = Languages.ENGLISH.value

    def test_treasure_card(self):
        expected_loot_id = LootCard._next_loot_id
        card = LootCard(50)
        self.assertEqual("Loot", card.title)
        self.assertEqual("You get 50 gold coins.", card.text)
        self.assertEqual(f"treasure_{expected_loot_id}", card.id)

    def test_event_card(self):
        card = EventCard(EventCardTypes.leviathan)
        self.assertEqual("If you have to miss a turn discard the leviathan instead.", card.text)
        self.assertEqual("leviathan", card.id)
