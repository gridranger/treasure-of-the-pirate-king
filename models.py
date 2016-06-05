# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'


class ShipType(object):
    def __init__(self, ship_type, price, crew_limit):
        self.ship_type = ship_type
        self.price = price
        self.crew_limit = crew_limit

    def __repr__(self):
        return "<ShipType object {}>".format(self.ship_type)
