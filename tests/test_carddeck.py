from unittest import TestCase
from unittest.mock import patch
from assets import CardDeck


class _DummyCard:
    def __init__(self, id):
        self.id = id


class _DummyDeck(CardDeck):
    pass


class TestCardDeck(TestCase):
    def setUp(self):
        self.alma = _DummyCard("alma")
        self.barack = _DummyCard("barack")
        self._test_deck = _DummyDeck([])
        self._test_deck.full_deck = [self.alma, self.barack]

    def test__unused_cards(self):
        self.assertEqual(self._test_deck.full_deck, self._test_deck._unused_cards)
        self._test_deck._used_cards.append(self.alma)
        self.assertEqual([self.barack], self._test_deck._unused_cards)

    def test_get_card(self):
        drawn = self._test_deck.get_card()
        self.assertTrue(drawn not in self._test_deck._unused_cards)
        self.assertEqual(len(self._test_deck._used_cards), len(self._test_deck._unused_cards))
        self.assertTrue(drawn in self._test_deck._used_cards)

    @patch("assets.CardDeck.refill_deck")
    def test_get_card_empty_deck(self, refill_deck):
        self._test_deck._used_cards = self._test_deck.full_deck
        with self.assertRaises(IndexError):
            self._test_deck.get_card()
        self.assertTrue(refill_deck.called)

    def test_remove_card(self):
        self._test_deck.remove_card(self.alma)
        self.assertTrue("alma" in self._test_deck._removed_cards_ids)

    def test_refill_deck(self):
        self._test_deck._used_cards = self._test_deck.full_deck
        self._test_deck.refill_deck()
        self.assertTrue(self._test_deck._unused_cards)
        self.assertFalse(self._test_deck._used_cards)

    def test_refill_deck_with_removed_cards(self):
        self._test_deck._used_cards = self._test_deck.full_deck
        self._test_deck._removed_cards_ids = ["barack"]
        self._test_deck.refill_deck()
        self.assertEqual([self.alma], self._test_deck._unused_cards)
