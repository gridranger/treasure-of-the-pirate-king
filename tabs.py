# -*- coding: utf-8 -*-
from logging import debug
from tkinter import Button, Entry, Frame, Label
from tkinter import DISABLED, E, SUNKEN, N, W
from tkinter.ttk import Notebook

from gametab import GameTab
from maintab import MainTab
from settingstab import SettingsTab

__author__ = 'Bárdos Dávid'


class Tabs(Notebook):
    def __init__(self, master=None, width=0):
        Notebook.__init__(self, master=master, width=width)
        self.width = width
        self.may_use_land_land_roll = False
        self.tabs = [MainTab(self, master), GameTab(self), SettingsTab(self, master), Frame(self)]
        for tab in self.tabs:
            self._position_tab(tab)
        self._enable_hotkeys()
        self.grid(row=0, column=0)
        if not self.master.is_game_in_progress.get():
            self.tab(1, state=DISABLED)
        self.ful3()

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

    def ful3(self):
        if not self.master.debug_mode:
            self.hide(3)
        self.tab(3, text='D')
        gombsor = Frame(self.tabs[3])
        Button(gombsor, text='Kincskártya húzása', command=lambda: self.master.engine.kincsetHuz()).grid()
        gombsor.grid(row=0)
        aranybeallit = Frame(self.tabs[3])
        Label(aranybeallit, text='Arany növelése:').grid(column=0, row=0)
        aranyMezo = Entry(aranybeallit, width=3)
        aranyMezo.grid(column=1, row=0)
        Button(aranybeallit, text='Beállít',
               command=lambda: self.master.engine.aktivjatekos.set_kincs(int(aranyMezo.get()))).grid(column=2, row=0)
        aranybeallit.grid(row=1)

    def ful3_var(self):
        valtozok = Frame(self.tabs[3])
        Label(valtozok, text='hadnagyElokerult:').grid(column=0, row=0)
        Label(valtozok, text='grogbaroLegyozve:').grid(column=0, row=1)
        Label(valtozok, textvar=self.master.engine.hadnagyElokerult).grid(column=1, row=0)
        Label(valtozok, textvar=self.master.engine.grogbaroLegyozve).grid(column=1, row=1)
        valtozok.grid(row=2)

    def reset_game_tab(self):
        self.tabs[1].reset_content()

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