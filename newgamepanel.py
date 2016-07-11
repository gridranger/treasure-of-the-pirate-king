# -*- coding: utf-8 -*-
from tkinter import DISABLED, E, W, Button, Checkbutton, Frame

from PIL.Image import ANTIALIAS
from PIL.ImageTk import PhotoImage

from colorize import image_tint
from newplayerfield import NewPlayerField

__author__ = 'Bárdos Dávid'


class NewGamePanel(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master, height=master.board_width, width=master.board_width)
        self.size = self.master.board_width
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        self.player_setups = []
        self.ship_picture_gray = image_tint('img/schooner.png', '#ffffff')
        self._scale_ship_picture_gray()
        for i in range(6):
            current_setup = NewPlayerField(self)
            is_active = Checkbutton(self, takefocus=0, variable=current_setup.active)
            if i == 0:
                current_setup.active.set(1)
                is_active.config(state=DISABLED)
            is_active.grid(row=i % 6, column=0, padx=5, pady=5, sticky=E)
            current_setup.grid(row=i % 6, column=1, sticky=W)
            self.player_setups.append(current_setup)
        start_button = Button(self, textvariable=self.master.ui_text_variables['start_button'],
                              command=self.player_setup_done)
        start_button.grid(row=0, column=2, rowspan=6, sticky=W)

    def _scale_ship_picture_gray(self):
        w = self.ship_picture_gray.width
        h = self.ship_picture_gray.height
        resized_image = self.ship_picture_gray.resize((int(self.size / 5), int(self.size / 5 * h / w)), ANTIALIAS)
        self.ship_picture_gray = PhotoImage(resized_image)

    def player_setup_done(self):
        empire_names = [empire.name for empire in self.master.empires.values()]
        jatekosadatok = []
        for i in range(6):
            if self.player_setups[i].active.get():
                if self.player_setups[i].nev.get() == '':
                    self.master.status_bar.log(self.master.ui_texts['name_missing'] % (i + 1))
                    return
                elif self.player_setups[i].picked_color.get() == '':
                    self.master.status_bar.log(self.master.ui_texts['color_missing'] % (self.player_setups[i].nev.get()))
                    return
                elif self.player_setups[i].nation_picker.get() == '':
                    self.master.status_bar.log(self.master.ui_texts['flag_missing'] % (self.player_setups[i].nev.get()))
                    return
                elif self.player_setups[i].nation_picker.get() not in empire_names:
                    self.master.status_bar.log(self.master.ui_texts['flag_invalid'] % (self.player_setups[i].nev.get()))
                    return
                self.master.status_bar.log(self.master.ui_texts['start_game'])
                self.update_idletasks()
                jatekosadatok.append([self.player_setups[i].nev.get(),
                                      self.player_setups[i].picked_color.get(),
                                      self.master.get_empire_id_by_name(self.player_setups[i].nation_picker.get())])
        self.master.start_game(jatekosadatok)
