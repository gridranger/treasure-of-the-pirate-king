from .deckfactory import DeckFactory
from .carddeck import CardDeck


class EventDeck(CardDeck):
    full_deck = DeckFactory.get_event_deck()

    def __init__(self, used_cards=None):
        CardDeck.__init__(self, used_cards)
