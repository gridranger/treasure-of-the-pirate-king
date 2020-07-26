from abc import ABC, abstractmethod
from random import choice


class CardDeck(ABC):
    def __init__(self, cards, used_cards=None):
        self._unused_cards = cards
        self._used_cards = used_cards if used_cards else []

    def get_card(self):
        if not self._unused_cards:
            self.refill_deck()
        card_to_draw = choice(self._unused_cards)
        self._unused_cards.remove(card_to_draw)
        self._used_cards.append(card_to_draw)
        return card_to_draw

    def refill_deck(self):
        self._unused_cards = self._used_cards
        self._used_cards = []

    @abstractmethod
    def load_deck(self):
        raise NotImplementedError
