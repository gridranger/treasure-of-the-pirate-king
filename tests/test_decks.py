from unittest import TestCase
from unittest.mock import patch
from assets.cards import EventDeck, TreasureDeck


class TestDecks(TestCase):

    @patch("assets.cards.deckfactory.DeckFactory.get_event_deck")
    def test_eventdeck(self, get_event_deck):
        deck = EventDeck()
        self.assertEqual(52, len(deck.full_deck))

    @patch("assets.cards.deckfactory.DeckFactory.get_treasure_deck")
    def test_treasuredeck(self, get_treasure_deck):
        deck = TreasureDeck()
        self.assertEqual(52, len(deck.full_deck))
