# flake8: noqa


class Helmsman(object):
    def __init__(self, tiles, wind_state, port_coordinates):
        self._board_tiles = tiles
        self._wind_state = wind_state
        self._port_coordinates = port_coordinates
        self._directions_on_game_grid = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        self._target_coordinates = {}
        self._visited_tiles = {}

    def get_target_coordinates(self, coordinates, die_roll, add_wind=True):
        self._calculate_tiles_in_range(coordinates, die_roll)
        self._select_target_coordinates(add_wind, die_roll)
        if coordinates in self._target_coordinates and coordinates not in self._port_coordinates:
            self._target_coordinates.pop(coordinates)
        return sorted(self._target_coordinates.keys())

    def _calculate_tiles_in_range(self, coordinates, die_roll):
        self._process_direct_neighbour_tiles(coordinates)
        for current_step in range(2, die_roll + 3):
            self._process_remote_tiles(current_step)

    def _process_direct_neighbour_tiles(self, coordinates):
        current_column, current_row = coordinates
        for (direction, (column_modifier, row_modifier)) in self._directions_on_game_grid.items():
            current_tile = _MappedTile(current_column + column_modifier, current_row + row_modifier, 1, direction)
            self._save_tile_if_useful(current_tile)

    def _save_tile_if_useful(self, current_tile):
        if current_tile.coordinates in self._board_tiles and current_tile.coordinates not in self._visited_tiles:
            self._visited_tiles[current_tile.coordinates] = current_tile

    def _process_remote_tiles(self, current_step):
        for tile in list(self._visited_tiles.values()):
            if tile.steps_to_this_tile == current_step - 1:
                self._process_neighbour_tiles(tile, current_step)

    def _process_neighbour_tiles(self, previous_tile, steps):
        current_column, current_row = previous_tile.coordinates
        for (direction, (column_modifier, row_modifier)) in self._directions_on_game_grid.items():
            current_tile = _MappedTile(current_column + column_modifier, current_row + row_modifier, steps,
                                       previous_tile.direction_from_start_tile)
            self._save_tile_if_useful(current_tile)

    def _select_target_coordinates(self, add_wind, die_roll):
        for tile in self._visited_tiles.values():
            if tile.coordinates in self._target_coordinates:
                continue
            modified_roll = die_roll
            if add_wind:
                modified_roll += self._get_wind_modifier(tile.direction_from_start_tile)
            if tile.steps_to_this_tile == modified_roll:
                self._target_coordinates[tile.coordinates] = tile
            elif tile.steps_to_this_tile < modified_roll and tile.coordinates in self._port_coordinates:
                self._target_coordinates[tile.coordinates] = tile

    def _get_wind_modifier(self, direction):
        wind = {"N": self._wind_state[0],
                "NE": self._wind_state[1],
                "E": self._wind_state[2],
                "SE": self._wind_state[3],
                "S": self._wind_state[4],
                "SW": self._wind_state[5],
                "W": self._wind_state[6],
                "EW": self._wind_state[7],
                "x": 0}
        return wind[direction]


class _MappedTile(object):
    def __init__(self, column, row, steps, direction_from_start_tile):
        self.column = column
        self.row = row
        self.steps_to_this_tile = steps
        self.direction_from_start_tile = direction_from_start_tile

    @property
    def coordinates(self):
        return self.column, self.row
