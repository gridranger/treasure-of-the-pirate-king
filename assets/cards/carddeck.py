from abc import ABC
from random import choice


class CardDeck(ABC):
    full_deck = []

    def __init__(self, used_cards):
        self._used_cards = used_cards
        self._removed_cards_ids = []

    @property
    def _unused_cards(self):
        return [card for card in self.full_deck if card not in self._used_cards]

    def get_card(self):
        if not self._unused_cards:
            self.refill_deck()
        drawn_card = choice(self._unused_cards)
        self._used_cards.append(drawn_card)
        return drawn_card

    def remove_card(self, card):
        self._removed_cards_ids.append(card.id)

    def refill_deck(self):
        removed_cards = []
        for card in self._used_cards:
            if card.id in self._removed_cards_ids:
                removed_cards.append(card)
        self._used_cards = removed_cards
