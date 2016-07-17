# -*- coding: utf-8 -*-
from logging import debug
from math import sqrt
from tkinter import IntVar

from models import PlayerState

__author__ = 'Bárdos Dávid'


class Player(object):
    def __init__(self, boss, tabla, state):
        self.game_board = tabla
        self.boss = boss
        self.nev = state.name
        self.szin = state.color
        self.empire = state.empire
        self.masodikszin = [int(self.szin[1:3], 16), int(self.szin[3:5], 16), int(self.szin[5:], 16)] # a játékos színét rgbvé bontjuk
        if sqrt(self.masodikszin[0]**2*0.241+self.masodikszin[1]**2*0.691+self.masodikszin[2]**2*0.068) > 127: # megállapítjuk hozzá az optimális gombócszínt
            self.masodikszin = 'black'
        else:
            self.masodikszin = 'white'
        self.zaszlo = self.boss.get_empire_id_by_capital_coordinates(self.sajatkikoto)
        debug("{} joined to the {} empire.".format(self.nev, self.zaszlo.capitalize()))
        self.hajo = state.ship
        self.legenyseg = IntVar(value=state.crew)
        self.legenyseg_max = IntVar()
        if state.coordinates == (-1, -1):
            self.pozicio = self.sajatkikoto
        else:
            self.pozicio = state.coordinates
        self.kincs = IntVar(value=state.gold)
        self.kincskeresesKesz = state.treasure_hunting_done
        self.statuszlista = state.states
        self.utolsodobas = state.last_roll
        self.kimarad = IntVar(value=state.turns_to_miss)
        self.hajotar = {}
        for empire in self.boss.empires:
            self.hajotar[empire] = IntVar()
        elfogottHajok = state.looted_ships
        if elfogottHajok != {}:
            for elfogottHajo in elfogottHajok.keys():
                self.hajotar[elfogottHajo].set(elfogottHajok[elfogottHajo])

    @property
    def sajatkikoto(self):
        empire = self.boss.empires[self.empire]
        return self.boss.game_board.locations[empire.capital][0]

    def set_hajo(self, tipus):
        "A megadott típusúra állítja be a játékos hajóját."
        self.hajo = tipus
        self.boss.game_board._render_ship_figure(self)

    def set_legenyseg(self, modosito):
        "Módosítja a legénység létszámát"
        self.legenyseg.set(self.legenyseg.get() + modosito)

    def set_legenyseg_max(self, szam):
        "Módosítja a legénység maximális létszámát"
        self.legenyseg_max.set(szam)

    def set_kincs(self, modosito):
        "Módosítja a kincs mennyiségét."
        self.kincs.set(self.kincs.get() + modosito)

    def set_statusz(self, statusz, ertek = 1):
        "Ad vagy megvon egy adott státuszt."
        #debug(self.nev,"státusza módosítás előtt:", self.statuszlista)
        if ertek:
            self.statuszlista.append(statusz)
        else:
            self.statuszlista.remove(statusz)
        #debug(self.nev,"státusza módosítás után:", self.statuszlista)

    def set_utolsodobas(self, ertek):
        "Megadja az utoljára dobott értéket."
        self.utolsodobas = ertek

    def set_kimarad(self, ertek = -1):
        "Beállítja, hány körből marad ki a játékos. Argumentum nélkül hívva levon egy kört."
        self.kimarad.set(self.kimarad.get()+ertek)

    def set_hajoszam(self, birodalom, szam):
        "Jóváírja a hajópontok változását."
        self.hajotar[birodalom].set(self.hajotar[birodalom].get()+szam)

    def set_kincskereses(self, ertek):
        "Kívülről hívható függvény, amely megváltoztatja a kincskeresesKesz paraméter értékét."
        self.kincskeresesKesz = ertek

    def export(self):
        current_state = PlayerState(self.nev, self.szin, self.empire)
        current_state.ship = self.hajo
        current_state.crew = self.legenyseg.get()
        current_state.coordinates = self.pozicio
        current_state.gold = self.kincs.get()
        current_state.states = self.statuszlista
        current_state.last_roll = self.utolsodobas
        current_state.turns_to_miss = self.kimarad.get()
        current_state.treasure_hunting_done = self.kincskeresesKesz
        for empire in self.hajotar:
            current_state.looted_ships[empire] = self.hajotar[empire].get()
        return current_state
