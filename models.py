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


class ShipType(object):
    def __init__(self, ship_type, price, crew_limit):
        self.ship_type = ship_type
        self.price = price
        self.crew_limit = crew_limit

    def __repr__(self):
        return "<ShipType object {}>".format(self.ship_type)
