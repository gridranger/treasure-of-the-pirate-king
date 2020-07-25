from .empire import Empire
from .port import Port


class GameState(object):
    def __init__(self):
        self.pirate_king_is_defeated = False
        self.first_mate_is_found = False
        self.pirate_kings_treasure_is_found = False
        self.ports = dict([(empire, Port()) for empire in Empire])
        self.current_turn_number = 0
