# -*- coding: utf-8 -*-
from logging import debug
from tkinter import ALL, E, HORIZONTAL, N, NORMAL, RAISED, S, SUNKEN, W, Frame, Label, Button
from tkinter.ttk import LabelFrame, Separator
from game import Dobokocka

__author__ = 'Bárdos Dávid'


class GameTab(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self._main_window = self.master.master
        self._land_land_roll = False
        self._heading = Frame(self)
        self._inventory_display = Frame(self)
        self._die_field = Frame(self)
        self._score_field = LabelFrame(self)
        self._turn_order = Frame(self)
        self.die = None
        if self._main_window.is_game_in_progress.get():
            self._load_content()

    @property
    def _current_player(self):
        return self._main_window.engine.aktivjatekos

    def reset_content(self):
        self._heading.destroy()
        self._heading = Frame(self)
        self._inventory_display.destroy()
        self._inventory_display = Frame(self)
        self._die_field.destroy()
        self._die_field = Frame(self)
        self._score_field.destroy()
        self._score_field = LabelFrame(self)
        self._turn_order.destroy()
        self._turn_order = Frame(self)
        if self.die:
            self.die.destroy()
        self.die = None
        self._load_content()

    def _load_content(self):
        self.master.tab(1, state=NORMAL)
        self._build_heading(0)
        self._build_inventory_display(1)
        self._build_score_field(2)
        self._build_state_display(3)
        self._horizontal_line(4)
        self._build_die_field(5)
        self._horizontal_line(6)
        self._build_turn_order(7)

    def _build_heading(self, position):
        flag = self._main_window.game_board.gallery['flag_' + self._current_player.empire]
        Label(self._heading, text=self._current_player.name).grid(row=0, column=0)
        Label(self._heading, image=flag).grid(row=1, column=0)
        self._heading.grid(row=position, column=0, pady=5)

    def _build_inventory_display(self, position):
        gold_frame = LabelFrame(self._inventory_display, text=self._main_window.ui_texts['treasure'])
        Label(gold_frame, image=self._main_window.game_board.gallery['penz-d2']).grid(row=0, column=0)
        Label(gold_frame, textvariable=self._current_player.gold).grid(row=0, column=1)
        gold_frame.grid(row=0, column=0, sticky=N + E + W + S, padx=5)
        crew_frame = LabelFrame(self._inventory_display, text=self._main_window.ui_texts['crew'])
        Label(crew_frame, image=self._main_window.game_board.gallery['crew']).grid(row=0, column=0)
        Label(crew_frame, textvariable=self._current_player.crew).grid(row=0, column=1)
        crew_frame.grid(row=0, column=1, sticky=N + E + W + S, padx=5)
        self._inventory_display.grid(row=position, column=0)
        self._inventory_display.columnconfigure(ALL, minsize=(self.master.width - 20) / 2)

    def _horizontal_line(self, position):
        Separator(self, orient=HORIZONTAL).grid(row=position, column=0, sticky=E + W, padx=5, pady=5)

    def _build_score_field(self, position):
        self._score_field.config(text=self._main_window.ui_texts['scores'])
        score_fields = {}
        target_empires = list(sorted(self._main_window.empires.keys()))
        target_empires.remove(self._current_player.empire)
        for index, empire in enumerate(target_empires):
            score_fields[empire] = Frame(self._score_field)
            flag = self._main_window.game_board.gallery['flag_' + empire]
            Label(score_fields[empire], image=flag).grid(row=0, column=0)
            Label(score_fields[empire], text=':').grid(row=0, column=1)
            Label(score_fields[empire], textvariable=self._current_player.scores[empire]).grid(row=0, column=2)
            score_fields[empire].grid(row=int((index / 2) % 2), column=index % 2, sticky=E + W)
        self._score_field.grid(row=position, column=0)
        self._score_field.columnconfigure(ALL, minsize=(self.master.width - 34) / 2)

    def _build_die_field(self, position):
        self._die_field.columnconfigure(0, weight=1)
        self._die_field.rowconfigure(0, weight=1)
        self._die_field.grid(row=position, column=0, ipady=5, ipadx=5)
        should_miss_turn = self._current_player.turns_to_miss.get()
        if should_miss_turn > 0:
            self._build_miss_turn_button(should_miss_turn)
        else:
            self._build_die()

    def _build_miss_turn_button(self, should_miss_turn):
        if should_miss_turn > 1:
            message = self._main_window.ui_texts["miss_turn"] % should_miss_turn
        else:
            message = self._main_window.ui_texts["miss_turn_last_time"]
        Button(self._die_field, text=message, command=self._main_window.engine.kimaradas).pack()
        if "leviathan" in self._current_player.states:
            command = self._main_window.engine.leviathan_kijatszasa
            Button(self._die_field, text=self._main_window.ui_texts["play_leviathan"], command=command).pack()

    def _build_die(self):
        self._die_field.config(relief=RAISED, bd=2)
        self.die = Dobokocka(self._die_field, self.master.width / 4, self._current_player.color,
                             self._current_player.secondary_color, self._current_player.last_roll)
        castaway_tiles = self._main_window.game_board.locations["castaways"]
        player_is_on_castaway_island = self._current_player.coordinates in castaway_tiles
        player_has_no_crew = not self._current_player.crew.get()
        if player_is_on_castaway_island and player_has_no_crew:
            self.die.bind('<Button-1>', self._main_window.engine.szamuzottek)
        else:
            self.die.bind('<Button-1>', self._roll_die)
        self.die.grid(row=0, column=0)

    def _build_turn_order(self, position):
        players = []
        turn_order_label = Label(self._turn_order, text=self._main_window.ui_texts['turn_order'])
        turn_order_label.grid(row=0, column=0, sticky=W)
        for index, player_name in enumerate(self._main_window.player_order):
            player = self._main_window.players[player_name]
            players.append(Label(self._turn_order, text=str(index + 1) + '. ' + player.name, bg=player.color,
                                 fg=player.secondary_color))
            players[-1].grid(row=index + 1, column=0, sticky=W, padx=10)
        self._turn_order.grid(row=position, column=0, sticky=W, padx=5)

    def _build_state_display(self, position):
        state_field = LabelFrame(self, text=self._main_window.ui_texts['cards'], relief=RAISED,
                                 width=self.master.width - 31)
        state_slots_per_row = int((self.master.width - 31) / 32)
        state_slot_height = 24 + ((int(len(self._current_player.states) / state_slots_per_row) + 1) * 32)
        if self._current_player.states:
            for index, state in enumerate(self._current_player.states):
                if state not in self._main_window.engine.nemKartyaStatusz:
                    if state in self._main_window.engine.eventszotar.keys():
                        origin = self._main_window.engine.eventszotar
                    else:
                        origin = self._main_window.engine.kincsszotar
                    icon = self._main_window.engine.eventszotar[state].kep + '_i'
                    icon = icon[(icon.find('_') + 1):]
                    button = Button(state_field, image=self._main_window.game_board.gallery[icon],
                                    command=lambda s=state: origin[s].megjelenik(1))
                    button.grid(row=int(index / state_slots_per_row), column=index % state_slots_per_row)
            state_field.config(height=state_slot_height)
            if state_field.winfo_children():
                state_field.grid(row=position, column=0)
            state_field.grid_propagate(False)

    def _roll_die(self, event):
        if self._land_land_roll:
            self._main_window.game_board.turn_off_blinker()
            self._main_window.engine.dobasMegtortent.set(False)
        if not self._main_window.engine.dobasMegtortent.get():
            dobas = self.die.dob()
            if "landland" in self._current_player.states:
                debug("New roll is possible because of Land, land! bonus.")
                self._main_window.status_bar.log(self._main_window.ui_texts['land_log'])
                self._current_player.remove_state("landland")
                self._land_land_roll = True
            else:
                self._main_window.status_bar.log('')
                self._die_field.config(relief=SUNKEN)
            self._main_window.engine.set_dobasMegtortent()
            self._main_window.is_turn_in_progress.set(1)
            self._main_window.engine.aktivjatekos.last_roll = dobas
            self._main_window.engine.mozgas(dobas, 1)

    def disable_additional_roll(self):
        if self._land_land_roll is False:
            self._main_window.status_bar.log('')
            self._die_field.config(relief=SUNKEN)
            self._land_land_roll = False
