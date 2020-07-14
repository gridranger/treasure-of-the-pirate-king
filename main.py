from logging import DEBUG, WARNING, basicConfig, getLogger
from tkinter import DISABLED, E, N, NORMAL, S, W, Frame, IntVar, StringVar, Tk
from tkinter.messagebox import askokcancel

from board import Board
from datareader import DataReader
from game import Vezerlo
from player import Player
from logframe import LogFrame
from models import BRITISH, DUTCH, FRENCH, PIRATE, SPANISH, GameState
from assets.empire import _Empire  # Todo remove it
from newgamepanel import NewGamePanel
from savehandler import SaveHandler
from tabs import Tabs


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
        self.empires = {BRITISH: _Empire(BRITISH, 'portroyal', '', (0, 0)),
                        FRENCH: _Empire(FRENCH, 'martinique', '', (0, 0)),
                        DUTCH: _Empire(DUTCH, 'curacao', '', (0, 0)),
                        SPANISH: _Empire(SPANISH, 'havanna', '', (0, 0)),
                        PIRATE: _Empire(PIRATE, 'tortuga', '', (0, 0))}
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
        self.menu.load_ui_texts()
        if self.is_game_setup_in_progress.get():
            picked_nations = self._save_game_setup_state()
        for rowid, row in self.empires.items():
            row.name = self.ui_texts[row.adjective.lower()]
        if self.is_game_setup_in_progress.get():
            self._reload_game_setup_state(picked_nations)
        if self.is_game_in_progress.get():
            self.menu.reset_game_tab()

    def _save_game_setup_state(self):
        picked_nations = []
        for i in range(6):
            empire_name = self.game_board.player_setups[i].empire_picker.get()
            if empire_name != '':
                picked_nations.append(self.get_empire_id_by_name(empire_name))
            else:
                picked_nations.append('')
        return picked_nations

    def _reload_game_setup_state(self, picked_nations):
        for i in range(6):
            self.game_board.player_setups[i].empire_picker.config(value=self.list_empire_names())
            if picked_nations[i] != '':
                self.game_board.player_setups[i].empire_picker.set(self.empires[picked_nations[i]].name)

    def get_empire_id_by_capital(self, capital):
        for empire in self.empires.values():
            if empire.capital == capital:
                return empire.adjective
        return ''

    def get_empire_id_by_capital_coordinates(self, coordinates):
        for empire in self.empires.values():
            if empire.coordinates == coordinates:
                return empire.adjective
        return ''

    def get_empire_id_by_name(self, name):
        for empire in self.empires.values():
            if empire.name == name:
                return empire.adjective
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
        self.menu.select(self.menu.settings_tab)
        self.status_bar.log('%s %i×%i' % (self.ui_texts['new_resolution'], self.width, self.height))

    def _save_game_setup_before_resize(self):
        player_data = []
        for i in range(6):
            if self.game_board.player_setups[i].active.get():
                player_data.append(self.game_board.player_setups[i].get_player_state())
        return player_data

    def _load_game_setup_before_resize(self, player_data):
        self.start_game_setup()
        for i, player_state in enumerate(player_data):
            self.game_board.player_setups[i].set_player_state(player_state)

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
        self.game_board = NewGamePanel(self)
        self.game_board.columnconfigure('all', weight=1)
        self.game_board.rowconfigure('all', weight=1)
        self.game_board.grid(row=0, column=1, rowspan=2, sticky=N + E + W + S, padx=5, pady=5)

    def select_file_to_load(self):
        if self.is_game_in_progress.get():
            if not askokcancel(self.ui_text_variables['new_game'].get(), self.ui_texts['discard_game-b']):
                return
        game_state = self.save_handler.load_saved_state()
        if game_state is None or not game_state.check():
            return
        self.status_bar.log(self.ui_texts['loading_game'])
        self.load_game(game_state)

    def load_game(self, game_state):
        self._reset_for_game_start()
        for data in game_state.player_data:
            self.players[data] = Player(self.empires, self.game_board, game_state.player_data[data])
        self._prepare_new_ui()
        while self.player_order[0] != game_state.next_player:
            self.player_order.append(self.player_order.pop(0))
        self.engine = Vezerlo(self, game_state.taverns)
        self.game_board.update_wind_direction(game_state.wind_index)
        if game_state.is_lieutenant_found:
            self.engine.set_hadnagyElokerult()
        if game_state.is_grog_lord_defeated:
            self.engine.set_grogbaroLegyozve()
        self.menu.update_developer_tab()
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
        self.menu.select(self.menu.game_tab)

    def start_game(self, player_states):
        self._reset_for_game_start()
        for index, player_state in enumerate(player_states):
            self.players['player' + str(index)] = Player(self.empires, self.game_board, player_state)
        self._prepare_new_ui()
        self.engine = Vezerlo(self)
        self.menu.update_developer_tab()
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
        game_state.wind_index = self.game_board.wind_direction.index(0)
        for player in sorted(list(self.players)):
            game_state.player_data[player] = self.players[player].export()
        for empire in self.empires.values():
            game_state.taverns[empire.capital] = self.engine.varostar[empire.capital].export_matroz()
        game_state.card_decks = [self.engine.eventdeck, self.engine.eventstack,
                                 self.engine.kincspakli, self.engine.treasurestack]
        game_state.is_grog_lord_defeated = self.engine.grogbaroLegyozve.get()
        game_state.is_lieutenant_found = self.engine.hadnagyElokerult.get()
        if game_state.check():
            self.save_handler.write_save(game_state)
        else:
            raise RuntimeError('Invalid game state.')

    def save_and_exit(self):
        self.save_game()
        self.shutdown_ttk_repeat_fix()

    def exit(self):
        if self.is_game_in_progress.get() and self.game_board.is_field_select_blinking:
            self.game_board.is_field_select_blinking = False
        self.destroy()


if __name__ == '__main__':
    a = Application(1)
    a.mainloop()
