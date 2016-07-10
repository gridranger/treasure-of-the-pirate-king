# -*- coding: utf-8 -*-
from tkinter import DISABLED, E, HORIZONTAL, NORMAL, W, Button, Checkbutton, Frame, IntVar, Label, Scale
from tkinter.ttk import Combobox, LabelFrame

__author__ = 'Bárdos Dávid'


class SettingsTab(Frame):
    def __init__(self, master, main_window):
        Frame.__init__(self, master=master)
        self._main_window = main_window
        self.resolution_field = LabelFrame(self, text='')
        self.language_field = LabelFrame(self, text='')
        self.is_full_screen = IntVar()
        self.is_full_screen.set(main_window.is_full_screen.get())
        for index, field in enumerate((self.resolution_field, self.language_field)):
            field.columnconfigure(0, weight=1)
            field.grid(row=index, column=0, sticky=E + W, padx=5, pady=5)
        self.resolutions = sorted(main_window.resolution_list)
        self.resolution_scale = Scale(self.resolution_field, from_=0, to=len(self.resolutions) - 1, orient=HORIZONTAL,
                                      resolution=1, takefocus=0, showvalue=0, length=self.master.width,
                                      command=self.felbontassav)
        self.resolution_scale.set(self._compose_scale())
        self.resolution_scale.grid(row=0, column=0, columnspan=2, sticky=E + W)
        self.resolution_display = Label(self.resolution_field, text=(main_window.width, '×', main_window.height))
        self.resolution_display.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.resolution_changer = Button(self.resolution_field, textvariable=main_window.ui_text_variables['apply'],
                                         command=self._change_resolution, state=DISABLED)
        self.resolution_changer.grid(row=1, column=1, padx=5, pady=5, sticky=E)
        self.full_screen_label = Label(self.resolution_field,
                                       textvariable=main_window.ui_text_variables['full_screen'])
        self.full_screen_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.full_screen_checkbox = Checkbutton(self.resolution_field, takefocus=0, variable=self.is_full_screen,
                                                command=lambda: self.resolution_changer.config(state=NORMAL))
        self.full_screen_checkbox.grid(row=2, column=1, padx=5, pady=5, sticky=E)
        self._language_picker()

    def felbontassav(self, ertek):
        self.resolution_display.config(
            text=(str(self.resolutions[int(ertek)][0]), '×', str(self.resolutions[int(ertek)][1])))
        if (self.master.width, self.master.height) == (
                self.resolutions[int(ertek)][0], self.resolutions[int(ertek)][1]):
            self.resolution_changer.config(state=DISABLED)
        else:
            self.resolution_changer.config(state=NORMAL)

    def _compose_scale(self):
        resolution_code = self._main_window.resolution_code
        return self.resolutions.index([item for item in self.resolutions if item[2] == resolution_code][0])

    def _change_resolution(self):
        self._main_window.resize(self.resolutions[self.resolution_scale.get()], self.is_full_screen.get())

    def _language_picker(self):
        self.nyelvlista = self._main_window.data_reader.load_language_list()
        self.nyelvlistaR = {v: k for k, v in self.nyelvlista.items()}
        self.nyelvvalaszto = Combobox(self.language_field, value=sorted(list(self.nyelvlista)), takefocus=0)
        self.nyelvvalaszto.set(self.nyelvlistaR[self.master.language])
        self.nyelvvalaszto.bind("<<ComboboxSelected>>", self._pick_language)
        self.nyelvvalaszto.grid(row=0, column=0, padx=5, pady=5)

    def _pick_language(self, event):
        new_language = self.nyelvlista[self.nyelvvalaszto.get()]
        self._main_window.set_new_language(new_language)
