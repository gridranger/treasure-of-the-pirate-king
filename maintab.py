from tkinter import Frame, Button, RAISED, FLAT, DISABLED, SUNKEN, NORMAL


class MainTab(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        main_window = self.master.master
        self._new_game_button = Button(self, textvariable=main_window.ui_text_variables['new_game'],
                                       command=main_window.start_game_setup, width=20, overrelief=RAISED, relief=FLAT)
        self._load_button = Button(self, textvariable=main_window.ui_text_variables['load_saved_game'],
                                   command=main_window.select_file_to_load, width=20, overrelief=RAISED, relief=FLAT)
        self._save_button = Button(self, textvariable=main_window.ui_text_variables['save'],
                                   command=main_window.save_game, width=20, overrelief=RAISED, relief=FLAT,
                                   state=DISABLED)
        self._save_and_exit_button = Button(self, textvariable=main_window.ui_text_variables['save_and_exit'],
                                            command=main_window.save_and_exit, width=20, overrelief=RAISED,
                                            relief=FLAT, state=DISABLED)
        self._exit_button = Button(self, textvariable=main_window.ui_text_variables['exit'], command=main_window.exit,
                                   width=20, overrelief=RAISED, relief=FLAT)
        self._position_elements()

    def _position_elements(self):
        self.grid(row=0, column=0, pady=10)
        self._new_game_button.grid(row=0, column=0)
        self._load_button.grid(row=1, column=0)
        self._save_button.grid(row=2, column=0)
        self._save_and_exit_button.grid(row=3, column=0)
        self._exit_button.grid(row=4, column=0)

    def push_new_game_button(self):
        self._new_game_button.config(relief=SUNKEN, overrelief=SUNKEN)

    def release_new_game_button(self):
        self._new_game_button.config(overrelief=RAISED, relief=FLAT)

    def enable_save_buttons(self):
        self._save_button.config(state=NORMAL)
        self._save_and_exit_button.config(state=NORMAL)

    def disable_save_buttons(self):
        self._save_button.config(state=DISABLED)
        self._save_and_exit_button.config(state=DISABLED)
