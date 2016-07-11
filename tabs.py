# -*- coding: utf-8 -*-
from logging import debug
from tkinter import DISABLED, E, SUNKEN, N, W
from tkinter.ttk import Notebook

from developertab import DeveloperTab
from gametab import GameTab
from maintab import MainTab
from settingstab import SettingsTab

__author__ = 'Bárdos Dávid'


class Tabs(Notebook):
    def __init__(self, master=None, width=0):
        Notebook.__init__(self, master=master, width=width)
        self.width = width
        self.may_use_land_land_roll = False
        self.tabs = [MainTab(self, master), GameTab(self), SettingsTab(self, master), DeveloperTab(self, master)]
        for tab in self.tabs:
            self._position_tab(tab)
        self._enable_hotkeys()
        self.grid(row=0, column=0)
        if not self.master.is_game_in_progress.get():
            self.tab(1, state=DISABLED)
        if not self.master.debug_mode:
            self.hide(3)
        self.tab(3, text='Dev')

    @property
    def ful1tartalom(self):
        return self.tabs[1]

    def _position_tab(self, tab):
        tab.columnconfigure(0, weight=1)
        tab.grid(row=0, column=0)
        self.add(tab, text='', underline=0, sticky=N + E + W)

    def _enable_hotkeys(self):
        self.enable_traversal()

    def push_new_game_button(self):
        self.tabs[0].push_new_game_button()

    def release_new_game_button(self):
        self.tabs[0].release_new_game_button()

    def enable_save_buttons(self):
        self.tabs[0].enable_save_buttons()

    def disable_save_buttons(self):
        self.tabs[0].disable_save_buttons()

    def reset_game_tab(self):
        self.tabs[1].reset_content()

    def update_developer_tab(self):
        self.tabs[3].add_game_dependent_tools()

    def dobas(self, event):
        "Dob a kockával."
        if self.may_use_land_land_roll:
            self.master.game_board.villogaski()
            self.master.engine.dobasMegtortent.set(False)
        if not self.master.engine.dobasMegtortent.get():
            dobas = self.ful1tartalom.die.dob()
            if "fold_fold" in self.master.engine.aktivjatekos.statuszlista:
                debug("New roll is possible because of Land, land! bonus.")
                self.master.status_bar.log(self.master.ui_texts['land_log'])
                self.master.engine.aktivjatekos.set_statusz("fold_fold", 0)
                self.may_use_land_land_roll = True
            else:
                self.master.status_bar.log('')
                self.ful1tartalom._die_field.config(relief=SUNKEN)
            self.master.engine.set_dobasMegtortent()
            self.master.is_turn_in_progress.set(1)
            self.master.engine.aktivjatekos.set_utolsodobas(dobas)
            self.master.engine.mozgas(dobas, 1)