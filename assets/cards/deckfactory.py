from .card import EventCard, LootCard, TreasureCard
from .eventcardtypes import EventCardTypes
from .treasurecardtypes import TreasureCardTypes


class DeckFactory:

    @classmethod
    def get_event_deck(cls):
        event_deck = []
        for event_type in EventCardTypes:
            event_deck.append(EventCard(event_type))
        return event_deck

    @classmethod
    def get_treasure_deck(cls):
        treasure_deck = []
        for treasure_type in TreasureCardTypes:
            if treasure_type == TreasureCardTypes.treasure:
                treasure_deck.extend([LootCard(10)] * 15)
                treasure_deck.extend([LootCard(20)] * 10)
                treasure_deck.extend([LootCard(30)] * 5)
            else:
                treasure_deck.append(TreasureCard(treasure_type))
        return treasure_deck
