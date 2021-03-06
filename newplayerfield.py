from tkinter import Frame, RAISED, IntVar, StringVar, Label, E, Entry, Button, SUNKEN, DISABLED, colorchooser, NORMAL
from tkinter.ttk import Combobox

from PIL.Image import ANTIALIAS, open as pillow_open
from PIL.ImageTk import PhotoImage

from assets import Empires, Gallery
from models import PlayerState
from settings import ApplicationSettings as s


class NewPlayerField(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master, relief=RAISED, bd=2)
        self._main_window = self.master.master
        self.active = IntVar(value=0)
        self.active.trace('w', self._toggle_availability)
        self.picked_color = StringVar(value='')
        self.picked_color.trace('w', self._recolor_sails)
        self.config(height=self.master.horizontal_space / 5,
                    width=(self.master.horizontal_space - (3 * self.master.horizontal_space / 10)) / 2)
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        name_label = Label(self, textvariable=self._main_window.ui_text_variables['name_label'])
        name_label.grid(row=0, column=0, sticky=E)
        self.name = Entry(self, width=15)
        self.name.grid(row=0, column=1, sticky=E)
        picked_color_label = Label(self, textvariable=self._main_window.ui_text_variables['color_label'])
        picked_color_label.grid(row=1, column=0, sticky=E)
        self._color = Button(self, width=12, bd=2, relief=SUNKEN, command=self._pick_color)
        self._color.grid(row=1, column=1)
        empire_label = Label(self, textvariable=self._main_window.ui_text_variables['flag_label'])
        empire_label.grid(row=2, column=0, sticky=E)
        empire_names = [s.language.get(e.value.adjective) for e in Empires]
        self.empire_picker = Combobox(self, value=empire_names, takefocus=0, width=12, state='readonly')
        self.empire_picker.bind("<<ComboboxSelected>>")
        self.empire_picker.grid(row=2, column=1)
        for elem in [self.name, self._color, self.empire_picker]:
            elem.config(state=DISABLED)
        self.ship = Label(self, image=self.master.ship_picture_gray)
        self.ship.grid(row=0, column=2, rowspan=3)
        self.ship_image = None

    def _pick_color(self):
        (rgb, hex_code) = colorchooser.askcolor()
        if hex_code is None:
            return
        self.picked_color.set(hex_code)
        self._color.config(bg=self.picked_color.get())

    def _recolor_sails(self, a=None, b=None, c=None):
        self.ship_image = pillow_open('img/schooner-h.png')
        width, height = self.ship_image.size
        self.ship_image = self.ship_image.resize((int(self.master.horizontal_space / 5),
                                                  int(self.master.horizontal_space / 5 * height / width)),
                                                 ANTIALIAS)
        self.sail_image = (Gallery.tint_image('schooner-v', self.picked_color.get()).resize(
            (int(self.master.horizontal_space / 5), int(self.master.horizontal_space / 5 * height / width)), ANTIALIAS))
        self.ship_image.paste(self.sail_image, (0, 0), self.sail_image)
        self.ship_image = PhotoImage(self.ship_image)
        self.ship = Label(self, image=self.ship_image)
        self.ship.grid(row=0, column=2, rowspan=3)

    def _toggle_availability(self, a=None, b=None, c=None):
        if self.active.get():
            for elem in [self.name, self._color, self.empire_picker]:
                elem.config(state=NORMAL)
            self.ship.config(image=self.ship_image)
        else:
            for elem in [self.name, self._color, self.empire_picker]:
                elem.config(state=DISABLED)
            self.ship.config(image=self.master.ship_picture_gray)

    def check_player_setup(self):
        error_message = ''
        if self.name.get() == '':
            error_message = s.language.name_missing
        elif self.picked_color.get() == '':
            error_message = s.language.color_missing
        elif self.empire_picker.get() == '':
            error_message = s.language.flag_missing
        elif self.empire_picker.get() not in [s.language.get(e.value.adjective) for e in Empires]:
            error_message = s.language.color_missing.flag_invalid
        return error_message

    def get_player_state(self):
        empire_by_translation = dict([(s.language.get(empire.value.adjective), empire.value) for empire in Empires])
        empire = empire_by_translation.get(self.empire_picker.get(), None)
        return PlayerState(self.name.get(), self.picked_color.get(), empire)

    def set_player_state(self, player_state):
        self.active.set(1)
        self.name.insert(0, player_state.name)
        if player_state.color:
            self.picked_color.set(player_state.color)
            self._color.config(bg=player_state.color)
        if player_state.empire:
            self.empire_picker.set(player_state.empire.adjective)
