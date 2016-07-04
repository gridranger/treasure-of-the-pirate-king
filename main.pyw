from PIL.Image import ANTIALIAS
from PIL.ImageTk import PhotoImage
from board import Board
from colorize import *
from datareader import DataReader
from game import *
from logging import DEBUG, WARNING, basicConfig, getLogger
from logframe import LogFrame
from models import BRITISH, DUTCH, FRENCH, PIRATE, SPANISH, Empire, GameState
from savehandler import *
from tabs import Tabs
from tkinter import E, N,S, SUNKEN, W, Checkbutton, Entry, Tk
from tkinter import colorchooser
from tkinter.messagebox import askokcancel
from tkinter.ttk import Combobox


class Application(Tk):
    def __init__(self, debug_mode=0):
        Tk.__init__(self)
        self.engine = None
        self.language = None
        self.width = 0
        self.height = 0
        self.resolution_code = None
        self.is_full_screen = IntVar()
        self.screen_ratio = None
        self.resolution_list = []
        self.debug_mode = debug_mode
        if self.debug_mode:
            basicConfig(level=DEBUG)
            pil_logger = getLogger("PIL.PngImagePlugin")
            pil_logger.level = WARNING
        self.data_reader = DataReader(self)
        self._process_config()
        self.card_texts = {}
        self.ui_texts = {}
        self.ui_text_variables = {}
        self._load_texts()
        self._load_text_variables()
        self.save_handler = SaveHandler(self)
        self.is_game_setup_in_progress = IntVar(value=0)
        self.is_game_in_progress = IntVar(value=0)
        self.is_turn_in_progress = IntVar(value=1)
        self._render_panes()
        self.is_game_in_progress.trace('w', self._follow_game_progress_change)
        self.is_turn_in_progress.trace('w', self._follow_turn_progress_change)
        self.players = {}
        self.empires = {BRITISH: Empire(BRITISH, 'portroyal', '', (0, 0)),
                        FRENCH: Empire(FRENCH, 'martinique', '', (0, 0)),
                        DUTCH: Empire(DUTCH, 'curacao', '', (0, 0)),
                        SPANISH: Empire(SPANISH, 'havanna', '', (0, 0)),
                        PIRATE: Empire(PIRATE, 'tortuga', '', (0, 0))}
        self._text_placer()
        self.protocol("WM_DELETE_WINDOW", self.shutdown_ttk_repeat_fix)
        self.exit_in_progress = False

    @property
    def board_width(self):
        return self.height - 10

    def _process_config(self):
        settings = self.data_reader.load_settings()
        self.language = settings.language
        self.width = settings.width
        self.height = settings.height
        self.resolution_code = settings.resolution_code
        self.resolution_list = settings.resolution_list
        self.screen_ratio = self.resolution_code[:4]
        self.is_full_screen.set(settings.full_screen)
        self._fix_window_size()

    def _fix_window_size(self):
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)
        if self.is_full_screen.get():
            self._set_full_screen_position()
        else:
            self._set_windowed_position()

    def _set_full_screen_position(self):
        self.overrideredirect(1)
        self.geometry("{}x{}+0+0".format(self.width, self.height))

    def _set_windowed_position(self):
        self.overrideredirect(0)
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, 100, 100))

    def _load_texts(self):
        self.ui_texts = self.data_reader.load_dictionary(self.language, entry_type='text')

    def _load_text_variable_values(self):
        text_variable_values = self.data_reader.load_dictionary(self.language, entry_type='textvariable')
        return text_variable_values

    def _load_text_variables(self):
        text_variable_values = self._load_text_variable_values()
        for entry in text_variable_values:
            self.ui_text_variables.setdefault(entry, StringVar()).set(text_variable_values[entry])

    def _text_placer(self):
        picked_nations = []
        self.title(self.ui_texts['title'])
        self.menu.tab(0, text=self.ui_texts['main_main'])
        self.menu.tab(1, text=self.ui_texts['game'])
        self.menu.tab(2, text=self.ui_texts['settings'])
        if self.is_game_setup_in_progress.get():
            picked_nations = self._save_game_setup_state()
        for rowid, row in self.empires.items():
            row.name = self.ui_texts[row.empire_id.lower()]
        if self.is_game_setup_in_progress.get():
            self._reload_game_setup_state(picked_nations)
        if self.is_game_in_progress.get():
            self.menu.ful1feltolt()

    def _save_game_setup_state(self):
        picked_nations = []
        for i in range(6):
            empire_name = self.game_board.player_setups[i].nation_picker.get()
            if empire_name != '':
                picked_nations.append(self.get_empire_id_by_name(empire_name))
            else:
                picked_nations.append('')
        return picked_nations

    def _reload_game_setup_state(self, picked_nations):
        for i in range(6):
            self.game_board.player_setups[i].nation_picker.config(value=self.list_empire_names())
            if picked_nations[i] != '':
                self.game_board.player_setups[i].nation_picker.set(self.empires[picked_nations[i]].name)

    def get_empire_id_by_capital(self, capital):
        for empire in self.empires.values():
            if empire.capital == capital:
                return empire.empire_id
        return ''

    def get_empire_id_by_capital_coordinates(self, coordinates):
        for empire in self.empires.values():
            if empire.coordinates == coordinates:
                return empire.empire_id
        return ''

    def get_empire_id_by_name(self, name):
        for empire in self.empires.values():
            if empire.name == name:
                return empire.empire_id
        return ''

    def list_empire_names(self):
        return [empire.name for empire in self.empires.values()]

    def set_new_language(self, new_language):
        if self.language == new_language:
            return
        self.language = new_language
        self._load_texts()
        self._load_text_variables()
        self._text_placer()
        self.card_texts = self.data_reader.load_cards_text()
        self.status_bar.log(self.ui_texts['new_language'])
        self.data_reader.save_settings(new_language=new_language)

    def _render_panes(self):
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        menu_width = int((self.height / 3) - 10)
        self.status_bar = LogFrame(self, menu_width)
        self.status_bar.grid(row=1, column=0, sticky=S + W, padx=5, pady=5)
        if self.is_game_in_progress.get():
            self._render_game_board()
        else:
            self._render_game_board_placeholder()
        self.menu = Tabs(self, menu_width)
        self.menu.grid(row=0, column=0, sticky=N + W, padx=5, pady=5)
        if self.screen_ratio == 'wide':
            ship_width = self.width - menu_width - self.board_width - 30
            self.ship = Frame(self, width=ship_width)
            self.ship.grid(row=0, column=2, rowspan=2, sticky=W + N + E, padx=5, pady=5)

    def _render_game_board_placeholder(self):
        self.game_board = Frame(self, width=self.board_width, height=self.board_width)
        self.game_board.player_setups = []
        self.game_board.grid(row=0, column=1, rowspan=2, sticky=N + W, padx=5, pady=5)

    def _render_game_board(self):
        self.game_board = Board(self, self.board_width)
        self.game_board.render_board()
        self.game_board.grid(row=0, column=1, rowspan=2, sticky=N + W, padx=5, pady=5)

    def resize(self, new_resolution, is_new_full_screen):
        is_same_resolution = (self.width, self.height) == (new_resolution[0], new_resolution[1])
        is_same_full_screen_setting = self.is_full_screen.get() == is_new_full_screen
        if is_same_resolution and is_same_full_screen_setting:
            return
        self.data_reader.save_settings(new_resolution[2], str(is_new_full_screen))
        player_data = []
        if self.is_game_setup_in_progress.get():
            player_data = self._save_game_setup_before_resize()
        self._process_config()
        self._remove_everything()
        self._render_panes()
        if self.is_game_setup_in_progress.get():
            self._load_game_setup_before_resize(player_data)
        self._text_placer()
        self.menu.select(self.menu.tabs[2])
        self.status_bar.log('%s %i×%i' % (self.ui_texts['new_resolution'], self.width, self.height))

    def _save_game_setup_before_resize(self):
        player_data = []
        for i in range(6):
            if self.game_board.player_setups[i].aktiv.get():
                player_data.append([self.game_board.player_setups[i].nev.get(),
                                    self.game_board.player_setups[i].valasztottSzin.get(),
                                    self.game_board.player_setups[i].nation_picker.get()])
        return player_data

    def _load_game_setup_before_resize(self, player_data):
        self.start_game_setup()
        if len(player_data) > 0:
            for i in range(len(player_data)):
                self.game_board.player_setups[i].visszatolt(player_data[i][0], player_data[i][1],
                                                            player_data[i][2])

    def _remove_everything(self):
        self.menu.destroy()
        self.game_board.destroy()
        self.status_bar.destroy()
        try:
            self.ship.destroy()
        except AttributeError:
            pass

    def confirm_discard_game(self):
        is_game_in_progress = self.is_game_in_progress.get()
        if is_game_in_progress and not askokcancel(self.ui_text_variables['new_game'].get(),
                                                   self.ui_texts['discard_game']):
            return False
        elif is_game_in_progress:
            self.is_game_in_progress.set(0)
            return True
        else:
            return True

    def start_game_setup(self):
        confirmed = self.confirm_discard_game()
        if confirmed:
            if self.is_game_setup_in_progress.get():
                self._reset_board()
            self._prepare_game_setup()

    def _reset_board(self):
        self.is_game_setup_in_progress.set(0)
        self.game_board.destroy()
        self._render_game_board_placeholder()
        self.menu.release_new_game_button()

    def _prepare_game_setup(self):
        self.is_game_setup_in_progress.set(1)
        self.menu.push_new_game_button()
        self.game_board.destroy()
        self._render_game_board_placeholder()
        self.game_board = UjJatekAdatok(self, self.board_width)
        self.game_board.columnconfigure('all', weight=1)
        self.game_board.rowconfigure('all', weight=1)
        self.game_board.grid(row=0, column=1, rowspan=2, sticky=N + E + W + S, padx=5, pady=5)

    def select_file_to_load(self):
        if self.is_game_in_progress.get():
            if not askokcancel(self.ui_text_variables['new_game'].get(), self.ui_texts['discard_game-b']):
                return
        game_state = self.save_handler.load_saved_state()
        if not game_state.check():
            return
        self.status_bar.log(self.ui_texts['loading_game'])
        self.update_idletasks()
        self.load_game(game_state)

    def load_game(self, game_state):
        self._reset_for_game_start()
        for data in game_state.player_data:
            self.players[data] = Jatekos(self, self.game_board, *game_state.player_data[data])
        self._prepare_new_ui()
        self.game_board.change_wind_direction(game_state.wind_index)
        while self.player_order[0] != game_state.next_player:
            self.player_order.append(self.player_order.pop(0))
        if game_state.is_lieutenant_found:
            self.engine.set_hadnagyElokerult()
        if game_state.is_grog_lord_defeated:
            self.engine.set_grogbaroLegyozve()
        self.engine = Vezerlo(self, game_state.taverns)
        self.menu.ful3_var()
        self.engine.set_paklik(game_state.card_decks)
        self.status_bar.log(self.ui_texts["loading_done"])
        self.engine.szakasz_0()

    def _reset_for_game_start(self):
        self.is_game_setup_in_progress.set(0)
        self.card_texts = self.data_reader.load_cards_text()
        self.players = {}
        self.update_idletasks()
        self.is_game_in_progress.set(1)
        self.game_board.destroy()
        self.game_board = Board(self, self.board_width)
        self.game_board.grid(row=0, column=1, rowspan=2, sticky=N + W, padx=5, pady=5)

    def _prepare_new_ui(self):
        self.player_order = sorted(self.players.keys())
        self.game_board.render_board()
        self.menu.release_new_game_button()
        self.menu.select(self.menu.tabs[1])
        self.engine = Vezerlo(self)
        self.menu.ful3_var()

    def start_game(self, player_data):
        self._reset_for_game_start()
        for adat in player_data:
            self.players['player' + str(player_data.index(adat))] = Jatekos(self, self.game_board, *adat)
        self._prepare_new_ui()
        self.status_bar.log(self.ui_texts["start_game_done"])
        self.engine.szakasz_0()

    def _follow_game_progress_change(self, *args, **kwargs):
        if self.is_game_in_progress.get():
            self.menu.tab(1, state=NORMAL)
        else:
            self.menu.tab(1, state=DISABLED)

    def _follow_turn_progress_change(self, *args, **kwargs):
        if not self.is_turn_in_progress.get():
            self.menu.enable_save_buttons()
            self.menu.tab(0, state=NORMAL)
            self.menu.tab(2, state=NORMAL)
        else:
            self.menu.disable_save_buttons()
            self.menu.tab(0, state=DISABLED)
            self.menu.tab(2, state=DISABLED)

    def shutdown_ttk_repeat_fix(self):
        self.eval('::ttk::CancelRepeat')
        self.exit_in_progress = True
        self.exit()

    def get_window_position(self):
        info = self.winfo_geometry()
        xpos = info.index('+') + 1
        ypos = info[xpos:].index('+') + xpos
        x = int(info[xpos:ypos])
        y = int(info[ypos:])
        return x, y

    def save_game(self):
        game_state = GameState()
        game_state.next_player = self.player_order[0]
        game_state.wind_index = self.game_board.szelirany.index(0)
        for player in sorted(list(self.players)):
            game_state.player_data[player] = self.players[player].export()
        for empire in self.empires.values():
            game_state.taverns[empire.capital] = self.engine.varostar[empire.capital].export_matroz()
        game_state.card_decks = [self.engine.eventdeck, self.engine.eventstack,
                                 self.engine.kincspakli, self.engine.treasurestack]
        game_state.is_grog_lord_defeated = self.engine.grogbaroLegyozve.get()
        game_state.is_lieutenant_found = self.engine.hadnagyElokerult.get()
        if game_state.check():
            self.save_handler.set_adatok_fileba(game_state)
        else:
            raise RuntimeError('Invalid game state.')

    def save_and_exit(self):
        self.save_game()
        self.shutdown_ttk_repeat_fix()

    def exit(self):
        if self.is_game_in_progress.get() and self.game_board.villogasaktiv:
            self.boss.game_board.villogasaktiv = -1
        self.destroy()


class UjJatekos(Frame):
    def __init__(self, boss):
        Frame.__init__(self, master=boss, relief=RAISED, bd=2)
        self.boss = boss
        self.aktiv = IntVar()
        self.aktiv.set(0)
        self.aktiv.trace('w', self.aktival)
        self.valasztottSzin = StringVar()
        self.valasztottSzin.trace('w', self.hajoepito)
        self.valasztottSzin.set('')
        self.hajoepito()
        self.aktiv.trace('w', self.aktival)
        self.config(height=self.boss.meret / 5, width=(self.boss.meret - (3 * self.boss.meret / 10)) / 2)
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        self.nevfelirat = Label(self, textvariable=self.boss.boss.ui_text_variables['name_label'])
        self.nevfelirat.grid(row=0, column=0, sticky=E)
        self.nev = Entry(self, width=15)
        self.nev.grid(row=0, column=1, sticky=E)
        self.szinfelirat = Label(self, textvariable=self.boss.boss.ui_text_variables['color_label'])
        self.szinfelirat.grid(row=1, column=0, sticky=E)
        self.szin = Button(self, width=12, bd=2, relief=SUNKEN, command=self.szinvalaszto)
        self.szin.grid(row=1, column=1)
        self.zaszlofelirat = Label(self, textvariable=self.boss.boss.ui_text_variables['flag_label'])
        self.zaszlofelirat.grid(row=2, column=0, sticky=E)
        self.nation_picker = Combobox(self, value=self.boss.boss.list_empire_names(), takefocus=0, width=12, state='readonly')
        self.nation_picker.bind("<<ComboboxSelected>>", self.zaszlovalasztas)
        self.nation_picker.grid(row=2, column=1)
        for elem in [self.nev, self.szin, self.nation_picker]:
            elem.config(state=DISABLED)
        self.hajo = Label(self, image=self.boss.hajokepszurke)
        self.hajo.grid(row=0, column=2, rowspan=3)

    def szinvalaszto(self):
        "Megnyit egy színválasztóablakot, és kiválasztja a hajó színét."
        (rgb, hex) = colorchooser.askcolor()
        if hex == None:
            return
        self.valasztottSzin.set(hex)
        self.szin.config(bg=self.valasztottSzin.get())

    def hajoepito(self, a=None, b=None, c=None):
        "Kiszínezi a hajó vitorlázatát."
        self.hajokep = open('img/schooner-h.png')
        szelesseg, magassag = self.hajokep.size
        self.hajokep = self.hajokep.resize((int(self.boss.meret / 5), int(self.boss.meret / 5 * magassag / szelesseg)),
                                           ANTIALIAS)
        self.vitorlakep = (image_tint('img/schooner-v.png', self.valasztottSzin.get()).resize(
            (int(self.boss.meret / 5), int(self.boss.meret / 5 * magassag / szelesseg)), ANTIALIAS))
        self.hajokep.paste(self.vitorlakep, (0, 0), self.vitorlakep)
        self.hajokep = PhotoImage(self.hajokep)
        self.hajo = Label(self, image=self.hajokep)
        self.hajo.grid(row=0, column=2, rowspan=3)

    def aktival(self, a=None, b=None, c=None):
        "Hozzáadható vagy kikapcsolható vele egy játékos."
        if self.aktiv.get():
            for elem in [self.nev, self.szin, self.nation_picker]:
                elem.config(state=NORMAL)
            self.hajo.config(image=self.hajokep)
        else:
            for elem in [self.nev, self.szin, self.nation_picker]:
                elem.config(state=DISABLED)
            self.hajo.config(image=self.boss.hajokepszurke)

    def zaszlovalasztas(self, event):
        "A legkördülőmenüre kattintáskor végrehajtandó függvény."
        self.zaszlo = self.nation_picker.get()

    def visszatolt(self, nev='', szin='', zaszlo=''):
        'Fogadja a felbontásváltás után visszatöltendő adatokat.'
        if not self.aktiv.get():
            self.aktiv.set(1)
        if nev != '':
            self.nev.insert(0, nev)
        if szin != '':
            self.valasztottSzin.set(szin)
            self.szin.config(bg=self.valasztottSzin.get())
        if zaszlo != '':
            self.nation_picker.set(zaszlo)


class UjJatekAdatok(Frame):
    """Az új játék beállításai."""

    def __init__(self, boss, meret):
        Frame.__init__(self, master=boss, height=meret, width=meret)
        self.boss = boss
        self.meret = meret
        self.columnconfigure('all', weight=1)
        self.rowconfigure('all', weight=1)
        self.player_setups = {}
        self.hajokepszurke = image_tint('img/schooner.png', '#ffffff')
        hajokepszurkew, hajokepszurkeh = self.hajokepszurke.size
        self.hajokepszurke = PhotoImage(
            self.hajokepszurke.resize((int(self.meret / 5), int(self.meret / 5 * hajokepszurkeh / hajokepszurkew)),
                                      ANTIALIAS))
        for i in range(6):
            self.player_setups[i] = UjJatekos(self)
            self.jatekosAktiv = Checkbutton(self, takefocus=0, variable=self.player_setups[i].aktiv)
            if i == 0:
                self.player_setups[i].aktiv.set(1)
                self.jatekosAktiv.config(state=DISABLED)
            self.jatekosAktiv.grid(row=i % 6, column=0, padx=5, pady=5, sticky=E)
            self.player_setups[i].grid(row=i % 6, column=1, sticky=W)
        self.startgomb = Button(self, textvariable=self.boss.ui_text_variables['start_button'],
                                command=self.jatekosokBeallitasaKesz)
        self.startgomb.grid(row=0, column=2, rowspan=6, sticky=W)

    def jatekosokBeallitasaKesz(self):
        empire_names = [empire.name for empire in self.boss.empires.values()]
        jatekosadatok = []
        for i in range(6):
            if self.player_setups[i].aktiv.get():
                if self.player_setups[i].nev.get() == '':
                    self.boss.status_bar.log(self.boss.ui_texts['name_missing'] % (i + 1))
                    return
                elif self.player_setups[i].valasztottSzin.get() == '':
                    self.boss.status_bar.log(self.boss.ui_texts['color_missing'] % (self.player_setups[i].nev.get()))
                    return
                elif self.player_setups[i].nation_picker.get() == '':
                    self.boss.status_bar.log(self.boss.ui_texts['flag_missing'] % (self.player_setups[i].nev.get()))
                    return
                elif self.player_setups[i].nation_picker.get() not in empire_names:
                    self.boss.status_bar.log(self.boss.ui_texts['flag_invalid'] % (self.player_setups[i].nev.get()))
                    return
                self.boss.status_bar.log(self.boss.ui_texts['start_game'])
                self.update_idletasks()
                jatekosadatok.append([self.player_setups[i].nev.get(),
                                      self.player_setups[i].valasztottSzin.get(),
                                      self.boss.get_empire_id_by_name(self.player_setups[i].nation_picker.get())])
        self.boss.start_game(jatekosadatok)


if __name__ == '__main__':
    a = Application(1)
    a.mainloop()
