# -*- coding: utf-8 -*-
from tkinter import Frame, RAISED, IntVar, StringVar, Label, E, Entry, Button, SUNKEN, DISABLED, colorchooser, NORMAL
from tkinter.ttk import Combobox

from PIL.Image import ANTIALIAS, open as pillow_open
from PIL.ImageTk import PhotoImage

from colorize import image_tint

__author__ = 'Bárdos Dávid'


class NewPlayerField(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master, relief=RAISED, bd=2)
        self._main_window = self.master.master
        self.active = IntVar(value=0)
        self.active.trace('w', self.aktival)
        self.picked_color = StringVar(value='')
        self.picked_color.trace('w', self._recolor_sails)
        self._recolor_sails()
        self.config(height=self.master.size / 5, width=(self.master.size - (3 * self.master.size / 10)) / 2)
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        self.nevfelirat = Label(self, textvariable=self._main_window.ui_text_variables['name_label'])
        self.nevfelirat.grid(row=0, column=0, sticky=E)
        self.nev = Entry(self, width=15)
        self.nev.grid(row=0, column=1, sticky=E)
        self.szinfelirat = Label(self, textvariable=self._main_window.ui_text_variables['color_label'])
        self.szinfelirat.grid(row=1, column=0, sticky=E)
        self.szin = Button(self, width=12, bd=2, relief=SUNKEN, command=self.szinvalaszto)
        self.szin.grid(row=1, column=1)
        self.zaszlofelirat = Label(self, textvariable=self._main_window.ui_text_variables['flag_label'])
        self.zaszlofelirat.grid(row=2, column=0, sticky=E)
        self.nation_picker = Combobox(self, value=self._main_window.list_empire_names(), takefocus=0, width=12, state='readonly')
        self.nation_picker.bind("<<ComboboxSelected>>", self.zaszlovalasztas)
        self.nation_picker.grid(row=2, column=1)
        for elem in [self.nev, self.szin, self.nation_picker]:
            elem.config(state=DISABLED)
        self.hajo = Label(self, image=self.master.ship_picture_gray)
        self.hajo.grid(row=0, column=2, rowspan=3)

    def szinvalaszto(self):
        "Megnyit egy színválasztóablakot, és kiválasztja a hajó színét."
        (rgb, hex) = colorchooser.askcolor()
        if hex == None:
            return
        self.picked_color.set(hex)
        self.szin.config(bg=self.picked_color.get())

    def _recolor_sails(self, a=None, b=None, c=None):
        "Kiszínezi a hajó vitorlázatát."
        self.hajokep = pillow_open('img/schooner-h.png')
        szelesseg, magassag = self.hajokep.size
        self.hajokep = self.hajokep.resize((int(self.master.size / 5), int(self.master.size / 5 * magassag / szelesseg)),
                                           ANTIALIAS)
        self.vitorlakep = (image_tint('img/schooner-v.png', self.picked_color.get()).resize(
            (int(self.master.size / 5), int(self.master.size / 5 * magassag / szelesseg)), ANTIALIAS))
        self.hajokep.paste(self.vitorlakep, (0, 0), self.vitorlakep)
        self.hajokep = PhotoImage(self.hajokep)
        self.hajo = Label(self, image=self.hajokep)
        self.hajo.grid(row=0, column=2, rowspan=3)

    def aktival(self, a=None, b=None, c=None):
        "Hozzáadható vagy kikapcsolható vele egy játékos."
        if self.active.get():
            for elem in [self.nev, self.szin, self.nation_picker]:
                elem.config(state=NORMAL)
            self.hajo.config(image=self.hajokep)
        else:
            for elem in [self.nev, self.szin, self.nation_picker]:
                elem.config(state=DISABLED)
            self.hajo.config(image=self.master.ship_picture_gray)

    def zaszlovalasztas(self, event):
        "A legkördülőmenüre kattintáskor végrehajtandó függvény."
        self.zaszlo = self.nation_picker.get()

    def visszatolt(self, nev='', szin='', zaszlo=''):
        'Fogadja a felbontásváltás után visszatöltendő adatokat.'
        if not self.active.get():
            self.active.set(1)
        if nev != '':
            self.nev.insert(0, nev)
        if szin != '':
            self.picked_color.set(szin)
            self.szin.config(bg=self.picked_color.get())
        if zaszlo != '':
            self.nation_picker.set(zaszlo)