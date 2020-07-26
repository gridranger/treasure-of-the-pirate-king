from unittest import TestCase
from unittest.mock import patch
from assets import CardDeck


class _DummyDeck(CardDeck):
    def load_deck(self):
        return CardDeck.load_deck(self)


class TestCardDeck(TestCase):
    def setUp(self):
        self._dummy_cards = ["alma", "korte"]
        self._test_deck = _DummyDeck(self._dummy_cards)

    def test_get_card(self):
        self._test_deck._unused_cards = self._dummy_cards
        drawn = self._test_deck.get_card()
        self.assertTrue(drawn not in self._test_deck._unused_cards)
        self.assertEqual(len(self._test_deck._used_cards), len(self._test_deck._unused_cards))
        self.assertTrue(drawn in self._test_deck._used_cards)

    @patch("assets.CardDeck.refill_deck")
    def test_get_card_empty_deck(self, refill_deck):
        self._test_deck._unused_cards = []
        with self.assertRaises(IndexError):
            self._test_deck.get_card()
        refill_deck.assert_called_once()

    def test_refill_deck(self):
        self._test_deck._used_cards = self._dummy_cards
        self._test_deck.refill_deck()
        self.assertTrue(self._test_deck._unused_cards)
        self.assertFalse(self._test_deck._used_cards)

    def test_load_deck(self):
        with self.assertRaises(NotImplementedError):
            self._test_deck.load_deck()
