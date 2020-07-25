from logging import debug
from time import perf_counter, sleep
from tkinter import BooleanVar, Canvas, CENTER, Frame, NW

from assets import Empire, Gallery
from helmsman import Helmsman
from settings import Settings


class Board(Frame):
    def __init__(self, master, width=768):
        Frame.__init__(self, master=master)
        self.player_setups = []
        self.size = width - width % 9
        self.board_canvas = self._add_board_canvas()
        self.tile_size = int(width / 9)
        self.tiles = self._generate_tiles()
        self.locations = {"battle_french": [(5, 9)],
                          "battle_british": [(9, 5)],
                          "battle_dutch": [(1, 5)],
                          "battle_spanish": [(5, 1)],
                          "Port Royal": [(5, 5)],
                          "Curacao": [(1, 9)],
                          "Tortuga": [(9, 1)],
                          "Havanna": [(1, 1)],
                          "Martinique": [(9, 9)],
                          "windplus90": [(7, 1), (9, 7)],
                          "windminus90": [(1, 7), (3, 5)],
                          "windplus45": [(1, 3), (5, 7), (7, 9), (9, 3)],
                          "windminus45": [(3, 1), (5, 3), (7, 5), (3, 9)],
                          "bermuda": [(9, 4)],
                          "landland": [(1, 6), (2, 9), (5, 4), (9, 2)],
                          "storm": [(2, 5), (5, 6), (9, 6)],
                          "driftwood": [(1, 8), (2, 1), (6, 5), (9, 8)],
                          "calm": [(4, 5), (8, 9)],
                          "taino": [(4, 1), (6, 9)],
                          "treasureisland": [(1, 2), (4, 9), (8, 1), (8, 5)],
                          "stream": [(1, 4), (5, 8), (6, 1)],
                          "castaways": [(5, 2)]}
        self.locationsR = self._reverse_locations()
        self.ports = self._collect_ports()
        self.ship_figure_images = {}
        self.figures = {}
        self.is_field_select_blinking = False
        self.is_field_select_visible = BooleanVar(value=False)
        #                      N, NE, E, SE,S, SW,W, NW
        self.wind_direction = [2, 1, -3, 1, 2, 1, 0, 1]
        self._targets = []
        self.tile_marks = []
        self._blinker = _Blinker(self)

    @property
    def _port_coordinates(self):
        return list(self.ports.values())

    def _add_board_canvas(self):
        canvas = Canvas(self, width=self.size, height=self.size, bd=0, highlightthickness=0, relief='ridge')
        canvas.grid()
        canvas.bind("<Button-1>", self._pick_tile)
        return canvas

    def _generate_tiles(self):
        tiles = []
        tiles += self._generate_whole_lines()
        tiles += self._generate_other_lines()
        tiles.sort()
        return tiles

    def _reverse_locations(self):
        result = {}
        for location, tiles in self.locations.items():
            for coordinates in tiles:
                result[coordinates] = location
        return result

    def _collect_ports(self):
        ports = {}
        capitals = [empire.value.capital for empire in Empire]
        for capital in capitals:
            ports[capital] = self.locations[capital][0]
        return ports

    def update_wind_direction(self, wind_index):
        while self.wind_direction[wind_index] != 0:
            self.wind_direction.append(self.wind_direction.pop(0))

    def _generate_whole_lines(self):
        return self._generate_lines((1, 5, 9), tuple(range(1, 10)))

    def _generate_other_lines(self):
        return self._generate_lines((2, 3, 4, 6, 7, 8), (1, 5, 9))

    @staticmethod
    def _generate_lines(rows, fields):
        tiles = []
        for row in rows:
            for field in fields:
                tiles.append((row, field))
        return tiles

    def render_board(self):
        debug('Board rendering started.')
        self._render_background()
        self._render_semi_transparent_tile_backgrounds()
        self._render_tiles()
        self._render_player_ship_figures()
        self._load_tile_picker()
        self._render_compass()
        self._display_wind()
        self._preload()
        debug('Board rendering finished.')

    def _render_background(self):
        self.board_canvas.create_image(0, 0, image=Gallery.get("map"), anchor=NW)

    def _render_semi_transparent_tile_backgrounds(self):
        for (x, y) in self.tiles:
            self.board_canvas.create_image(int((x - 0.5) * self.tile_size), int((y - 0.5) * self.tile_size),
                                           image=Gallery.get("tile"), anchor=CENTER)

    def _render_tiles(self):
        for location in self.locations:
            for x, y in self.locations[location]:
                self.board_canvas.create_image(int((x - 0.5) * self.tile_size), int((y - 0.5) * self.tile_size),
                                               image=Gallery.get(location), anchor=CENTER)

    def _render_player_ship_figures(self):
        for player_object in self.master.players.values():
            self.render_ship_figure(player_object)

    def render_ship_figure(self, player):
        Gallery._generate_assembled_ship_image(player.ship, player.color)
        self.ship_figure_images[player.name] = Gallery.get(f"{player.ship}_{player.color}")
        if player.name in self.figures:
            self.board_canvas.delete(self.figures[player.name])
        x, y = player.coordinates
        self.figures[player.name] = self.board_canvas.create_image((x - 0.5) * self.tile_size,
                                                                   (y - 0.5) * self.tile_size,
                                                                   image=self.ship_figure_images[player.name],
                                                                   anchor=CENTER)

    def _load_tile_picker(self):
        Gallery.get("X")

    def _render_compass(self):
        self.board_canvas.create_image(int(6.5 * self.tile_size), int(2.5 * self.tile_size),
                                       image=Gallery.get("compass"), anchor=CENTER)
        self.wind_direction_arrow = self.board_canvas.create_image(0, 0, image=None)

    def _display_wind(self):
        current_direction = str(self.wind_direction.index(0))
        image_key = 'wind_direction' + current_direction
        self.board_canvas.delete(self.wind_direction_arrow)
        self.wind_direction_arrow = self.board_canvas.create_image(int(6.5 * self.tile_size),
                                                                   int(2.5 * self.tile_size),
                                                                   image=Gallery.get(image_key), anchor=CENTER)

    def _preload(self):
        if not Settings.preload_images:
            return
        tic = perf_counter()
        self._render_money()
        self._render_crew()
        self._render_ships()
        self._render_flags()
        self._render_crewman()
        self._render_battle_screen_button_images()
        toc = perf_counter()
        debug(f"Preload took {toc - tic:0.4f} seconds.")

    def _render_money(self):
        for money_type in ['1', '8', 'd', 'd2']:
            Gallery.get(f"penz-{money_type}")

    def _render_crew(self):
        Gallery.get("crew")

    def _render_ships(self):
        for ship_type in ['brigantine', 'frigate', 'schooner', 'galleon']:
            Gallery.get(ship_type)

    def _render_flags(self):
        for empire in Empire:
            Gallery.get(f"flag_{empire.value.adjective.lower()}")

    def _render_crewman(self):
        for i in range(3):
            Gallery.get(f"crewman{i}")

    def _render_battle_screen_button_images(self):
        buttons = ["gun", "rifle", "caltrop", "grenade", "grapeshot", "greek_fire", "monkey", "sirenhorn", "sirens",
                   "alvarez"]
        for button in buttons:
            Gallery.get(f"icon_{button}")

    def _render_card_image(self, name):
        pass

    def calculate_target_tiles(self, coordinates, roll, add_wind_modifier):
        helmsman = Helmsman(self.tiles, self.wind_direction, self._port_coordinates)
        self._targets = helmsman.get_target_coordinates(coordinates, roll, add_wind_modifier)
        return self._targets

    def change_wind_direction(self, angle=0):
        updated_wind_index = (self.wind_direction.index(0) + int(angle / 45)) % 8
        self.update_wind_direction(updated_wind_index)
        self._display_wind()

    def mark_target_tiles(self, tiles):
        self.tile_marks = []
        for column, row in tiles:
            tile_mark = self.board_canvas.create_image((column - 0.5) * self.tile_size, (row - 0.5) * self.tile_size,
                                                       image=Gallery.get("X"), anchor=CENTER)
            self.tile_marks.append(tile_mark)
            self.is_field_select_visible.set(True)
        self.is_field_select_blinking = True
        self._blinker.start()

    def _pick_tile(self, event):
        if not self.master.engine.dobasMegtortent.get():
            return
        coordinates = int(event.x / self.tile_size) + 1, int(event.y / self.tile_size) + 1
        if coordinates not in self._targets:
            return
        self.master.menu.disable_additional_roll()
        self.turn_off_blinker()
        self.relocate_ship(coordinates)
        self.master.engine.szakasz_mezoevent()

    def turn_off_blinker(self):
        self.master.game_board.is_field_select_blinking = False
        if self.is_field_select_visible.get():
            self._blinker.hide_marks()
        self.tile_marks = []

    def relocate_ship(self, coordinates):
        x, y = coordinates
        self.board_canvas.coords(self.figures[self.master.engine.aktivjatekos.name], (x - 0.5) * self.tile_size,
                                 (y - 0.5) * self.tile_size)
        self.master.engine.aktivjatekos.coordinates = coordinates


class _Blinker(object):
    def __init__(self, master):
        self._master = master
        self._main_window = self._master.master

    def start(self):
        while self._master.is_field_select_blinking:
            if self._master.is_field_select_visible.get():
                self.hide_marks()
            else:
                self._show_marks()
            self._main_window.update()
            sleep(0.25)

    def hide_marks(self):
        for mark in self._master.tile_marks:
            self._master.board_canvas.itemconfigure(mark, state='hidden')
        self._master.is_field_select_visible.set(False)

    def _show_marks(self):
        for x in self._master.tile_marks:
            self._master.board_canvas.itemconfigure(x, state='normal')
        self._master.is_field_select_visible.set(True)
