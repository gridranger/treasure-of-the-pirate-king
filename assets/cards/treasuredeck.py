from .deckfactory import DeckFactory
from .carddeck import CardDeck


class TreasureDeck(CardDeck):
    full_deck = DeckFactory.get_treasure_deck()

    def __init__(self, used_cards=None):
        CardDeck.__init__(self, used_cards)
