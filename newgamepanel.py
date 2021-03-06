from tkinter import DISABLED, E, W, Button, Checkbutton, Frame

from PIL.Image import ANTIALIAS
from PIL.ImageTk import PhotoImage

from assets import Gallery
from newplayerfield import NewPlayerField
from settings import ApplicationSettings as s


class NewGamePanel(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master, height=master.board_width, width=master.board_width)
        self.horizontal_space = self.master.board_width
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        self.player_setups = []
        self.ship_picture_gray = Gallery.tint_image('schooner', '#ffffff')
        self._scale_ship_picture_gray()
        self._display_fields()

    def _display_fields(self):
        for i in range(6):
            current_field = NewPlayerField(self)
            is_active = Checkbutton(self, takefocus=0, variable=current_field.active)
            if i == 0:
                current_field.active.set(1)
                is_active.config(state=DISABLED)
            is_active.grid(row=i % 6, column=0, padx=5, pady=5, sticky=E)
            current_field.grid(row=i % 6, column=1, sticky=W)
            self.player_setups.append(current_field)
        start_button = Button(self, textvariable=self.master.ui_text_variables['start_button'],
                              command=self.player_setup_done)
        start_button.grid(row=0, column=2, rowspan=6, sticky=W)

    def _scale_ship_picture_gray(self):
        w = self.ship_picture_gray.width
        h = self.ship_picture_gray.height
        resized_image = self.ship_picture_gray.resize((int(self.horizontal_space / 5),
                                                       int(self.horizontal_space / 5 * h / w)), ANTIALIAS)
        self.ship_picture_gray = PhotoImage(resized_image)

    def player_setup_done(self):
        player_data = []
        for i in range(6):
            if self.player_setups[i].active.get():
                error_message = self.player_setups[i].check_player_setup()
                if error_message:
                    self._show_error_message(error_message, i)
                    return
                message = s.language.start_game
                self.master.status_bar.log(message)
                player_state = self.player_setups[i].get_player_state()
                player_data.append(player_state)
        self.master.start_game(player_data)

    def _show_error_message(self, error_message, player_number):
        if 'name_missing' == error_message:
            message = error_message.format(player_number + 1)
        else:
            message = error_message.format(self.player_setups[player_number].name.get())
        self.master.status_bar.log(message)
