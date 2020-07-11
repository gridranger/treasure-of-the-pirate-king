from tkinter import DISABLED, E, HORIZONTAL, NORMAL, W, Button, Checkbutton, Frame, IntVar, Label, Scale
from tkinter.ttk import Combobox, LabelFrame


class SettingsTab(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master)
        self._main_window = self.master.master
        self._resolution_field = LabelFrame(self, text='')
        self._language_field = LabelFrame(self, text='')
        self._is_full_screen = IntVar()
        self._is_full_screen.set(self._main_window.is_full_screen.get())
        self._position_fields()
        self._resolutions = sorted(self._main_window.resolution_list)
        self._resolution_scale = Scale(self._resolution_field, from_=0, to=len(self._resolutions) - 1,
                                       orient=HORIZONTAL, resolution=1, takefocus=0, showvalue=0,
                                       length=self._main_window.width, command=self._update_resolution_button)
        self._resolution_scale.set(self._compose_scale())
        self._resolution_display = Label(self._resolution_field, text=(self._main_window.width, '×',
                                                                       self._main_window.height))
        self._resolution_changer = Button(self._resolution_field,
                                          textvariable=self._main_window.ui_text_variables['apply'],
                                          command=self._change_resolution, state=DISABLED)
        self._full_screen_label = Label(self._resolution_field,
                                        textvariable=self._main_window.ui_text_variables['full_screen'])
        self._full_screen_checkbox = Checkbutton(self._resolution_field, takefocus=0, variable=self._is_full_screen,
                                                 command=lambda: self._resolution_changer.config(state=NORMAL))
        self._languages = self._main_window.data_reader.load_language_list()
        self._language_picker = Combobox(self._language_field, value=sorted(list(self._languages)), takefocus=0)
        self._language_picker.set(self._languages_reversed[self._main_window.language])
        self._language_picker.bind("<<ComboboxSelected>>", self._pick_language)
        self._position_elements()
        self.load_ui_texts()

    def _position_fields(self):
        for index, field in enumerate((self._resolution_field, self._language_field)):
            field.columnconfigure(0, weight=1)
            field.grid(row=index, column=0, sticky=E + W, padx=5, pady=5)

    @property
    def _languages_reversed(self):
        return dict(zip(self._languages.values(), self._languages.keys()))

    def _update_resolution_button(self, ertek):
        self._resolution_display.config(
            text=(str(self._resolutions[int(ertek)][0]), '×', str(self._resolutions[int(ertek)][1])))
        if (self._main_window.width, self._main_window.height) == (
                self._resolutions[int(ertek)][0], self._resolutions[int(ertek)][1]):
            self._resolution_changer.config(state=DISABLED)
        else:
            self._resolution_changer.config(state=NORMAL)

    def _compose_scale(self):
        resolution_code = self._main_window.resolution_code
        return self._resolutions.index([item for item in self._resolutions if item[2] == resolution_code][0])

    def _change_resolution(self):
        self._main_window.resize(self._resolutions[self._resolution_scale.get()], self._is_full_screen.get())

    def _pick_language(self, event):
        new_language = self._languages[self._language_picker.get()]
        self._main_window.set_new_language(new_language)

    def _position_elements(self):
        self._resolution_scale.grid(row=0, column=0, columnspan=2, sticky=E + W)
        self._resolution_display.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self._resolution_changer.grid(row=1, column=1, padx=5, pady=5, sticky=E)
        self._full_screen_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self._full_screen_checkbox.grid(row=2, column=1, padx=5, pady=5, sticky=E)
        self._language_picker.grid(row=0, column=0, padx=5, pady=5)

    def load_ui_texts(self):
        self._resolution_field.config(text=self._main_window.ui_texts['resolution'])
        self._language_field.config(text=self._main_window.ui_texts['language'])
