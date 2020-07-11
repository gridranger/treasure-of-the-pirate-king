# flake8: noqa
from tkinter import Button, Entry, Frame, Label


class DeveloperTab(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self._main_window = self.master.master
        tools = Frame(self)
        Button(tools, text='Draw treasure card', command=self._draw_treasure_card).grid()
        tools.grid(row=0)
        gold_setter = Frame(self)
        Label(gold_setter, text='Add gold').grid(column=0, row=0)
        self._gold_entry = Entry(gold_setter, width=3)
        self._gold_entry.grid(column=1, row=0)
        Button(gold_setter, text='Set', command=self._set_gold).grid(column=2, row=0)
        gold_setter.grid(row=1)

    def _draw_treasure_card(self):
        if self._main_window.engine:
            self._main_window.engine.kincsetHuz()

    def _set_gold(self):
        if self._main_window.engine:
            self._main_window.engine.aktivjatekos.update_gold(int(self._gold_entry.get()))

    def add_game_dependent_tools(self):
        variables = Frame(self)
        Label(variables, text='First mate is found:').grid(column=0, row=0)
        Label(variables, text='Grog Lord is defeated:').grid(column=0, row=1)
        Label(variables, textvariable=self._main_window.engine.hadnagyElokerult).grid(column=1, row=0)
        Label(variables, textvariable=self._main_window.engine.grogbaroLegyozve).grid(column=1, row=1)
        variables.grid(row=2)
