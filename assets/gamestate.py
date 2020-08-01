from .cards import EventDeck, TreasureDeck
from .empires import Empires
from .port import Port


class GameState(object):
    def __init__(self):
        self.pirate_king_is_defeated = False
        self.first_mate_is_found = False
        self.pirate_kings_treasure_is_found = False
        self.ports = dict([(empire, Port()) for empire in Empires])
        self.current_turn_number = 0
        self.event_deck = EventDeck()
        self.treasure_deck = TreasureDeck()
