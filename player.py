from logging import debug
from math import sqrt
from tkinter import IntVar
from assets import Empire
from models import PlayerState


class Player(object):
    def __init__(self, game_board, state):
        self._game_board = game_board
        self.name = state.name
        self.color = state.color
        self.empire = state.empire
        self.secondary_color = self._pick_secondary_color()
        debug("{} joined to the {} empire.".format(self.name, self.empire.capitalize()))
        self.ship = state.ship
        self.crew = IntVar(value=state.crew)
        self.crew_limit = IntVar()
        if state.coordinates == (-1, -1):
            self.coordinates = self._home_port
        else:
            self.coordinates = state.coordinates
        self.gold = IntVar(value=state.gold)
        self.treasure_hunting_done = state.treasure_hunting_done
        self.states = state.states
        self.last_roll = state.last_roll
        self.turns_to_miss = IntVar(value=state.turns_to_miss)
        self.scores = {}
        for empire in [empire.value for empire in Empire]:
            self.scores[empire.adjective] = IntVar(value=state.looted_ships.get(empire, 0))

    @property
    def _home_port(self):
        empire = Empire.get_by_id(self.empire)
        return self._game_board.locations[empire.capital][0]

    def _pick_secondary_color(self):
        r, g, b = [int(self.color[1:3], 16), int(self.color[3:5], 16), int(self.color[5:], 16)]
        if sqrt(r ** 2 * 0.241 + g ** 2 * 0.691 + b ** 2 * 0.068) > 127:
            return 'black'
        else:
            return 'white'

    def update_ship(self, new_ship_type):
        self.ship = new_ship_type
        self._game_board.render_ship_figure(self)

    def update_crew(self, modifier):
        self.crew.set(self.crew.get() + modifier)

    def update_gold(self, modifier):
        self.gold.set(self.gold.get() + modifier)

    def add_state(self, state):
        self.states.append(state)

    def remove_state(self, state):
        self.states.remove(state)

    def update_turns_to_miss(self, modifier=-1):
        self.turns_to_miss.set(self.turns_to_miss.get() + modifier)

    def export(self):
        current_state = PlayerState(self.name, self.color, self.empire)
        current_state.ship = self.ship
        current_state.crew = self.crew.get()
        current_state.coordinates = self.coordinates
        current_state.gold = self.gold.get()
        current_state.states = self.states
        current_state.last_roll = self.last_roll
        current_state.turns_to_miss = self.turns_to_miss.get()
        current_state.treasure_hunting_done = self.treasure_hunting_done
        for empire in self.scores:
            current_state.looted_ships[empire] = self.scores[empire].get()
        return current_state
