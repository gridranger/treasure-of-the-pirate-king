# -*- coding: utf-8 -*-
from tkinter import DISABLED, E, N, W
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
        self._main_tab = MainTab(self)
        self.game_tab = GameTab(self)
        self.settings_tab = SettingsTab(self)
        self._developer_tab = DeveloperTab(self)
        for tab in [self._main_tab, self.game_tab, self.settings_tab, self._developer_tab]:
            self._position_tab(tab)
        self._enable_hot_keys()
        self.grid(row=0, column=0)
        if not self.master.is_game_in_progress.get():
            self.tab(1, state=DISABLED)
        if not self.master.debug_mode:
            self.hide(3)
        self.tab(3, text='Dev')

    def _position_tab(self, tab):
        tab.columnconfigure(0, weight=1)
        tab.grid(row=0, column=0)
        self.add(tab, text='', underline=0, sticky=N + E + W)

    def _enable_hot_keys(self):
        self.enable_traversal()

    def load_ui_texts(self):
        self.tab(0, text=self.master.ui_texts['main_main'])
        self.tab(1, text=self.master.ui_texts['game'])
        self.tab(2, text=self.master.ui_texts['settings'])
        self.settings_tab.load_ui_texts()

    def push_new_game_button(self):
        self._main_tab.push_new_game_button()

    def release_new_game_button(self):
        self._main_tab.release_new_game_button()

    def enable_save_buttons(self):
        self._main_tab.enable_save_buttons()

    def disable_save_buttons(self):
        self._main_tab.disable_save_buttons()

    def reset_game_tab(self):
        self.game_tab.reset_content()

    def disable_additional_roll(self):
        self.game_tab.disable_additional_roll()

    def update_developer_tab(self):
        self._developer_tab.add_game_dependent_tools()
