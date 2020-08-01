from assets.cards.deckfactory import DeckFactory
from unittest import TestCase


class TestDeckFactory(TestCase):
    def test_get_event_cards(self):
        self.assertEqual(32, len(DeckFactory.get_event_deck()))

    def test_get_treasure_cards(self):
        self.assertEqual(52, len(DeckFactory.get_treasure_deck()))
