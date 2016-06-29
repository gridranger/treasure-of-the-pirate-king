# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

BRITISH = 'british'
FRENCH = 'french'
DUTCH = 'dutch'
PIRATE = 'pirate'
SPANISH = 'spanish'


class Empire(object):
    def __init__(self, empire_id, capital, name, coordinates):
        self.empire_id = empire_id
        self.capital = capital
        self.name = name
        self.coordinates = coordinates


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


class ShipType(object):
    def __init__(self, ship_type, price, crew_limit):
        self.ship_type = ship_type
        self.price = price
        self.crew_limit = crew_limit

    def __repr__(self):
        return "<ShipType object {}>".format(self.ship_type)
