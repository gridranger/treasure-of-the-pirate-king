class GameState(object):
    def __init__(self):
        self.player_data = {}
        self.next_player = ""
        self.wind_index = None
        self.taverns = {}
        self.card_decks = {}
        self.is_lieutenant_found = None
        self.is_grog_lord_defeated = None

    def check(self):
        if any(var is None for var in (self.wind_index, self.is_lieutenant_found, self.is_grog_lord_defeated)):
            return False
        elif any(dictionary == {} for dictionary in (self.player_data, self.taverns, self.card_decks)):
            return False
        elif self.next_player == "":
            return False
        else:
            return True


class LoadedSettings(object):
    def __init__(self):
        self.language = None
        self.width = 0
        self.height = 0
        self.full_screen = False
        self.resolution_code = ''
        self.resolution_list = ()


class PlayerState(object):
    def __init__(self, name, color, empire):
        self.name = name
        self.color = color
        self.empire = empire
        self.ship = 'schooner'
        self.crew = 10
        self.coordinates = (-1, -1)
        self.gold = 0
        self.states = []
        self.last_roll = 6
        self.turns_to_miss = 0
        self.treasure_hunting_done = True
        self.looted_ships = {}


class ShipType(object):
    def __init__(self, ship_type, price, crew_limit):
        self.ship_type = ship_type
        self.price = price
        self.crew_limit = crew_limit

    def __repr__(self):
        return "<ShipType object {}>".format(self.ship_type)
