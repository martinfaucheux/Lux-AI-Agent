import math
from typing import Dict, List, Optional, Tuple, Union

from utils.path_finder import bfs, game_map_to_array

from ..constants import Constants
from .cell import Cell, Resource
from .position import Position

DIRECTIONS = Constants.DIRECTIONS
RESOURCE_TYPES = Constants.RESOURCE_TYPES


class GameMap:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.map: List[List[Cell]] = [None] * height
        for y in range(0, self.height):
            self.map[y] = [None] * width
            for x in range(0, self.width):
                self.map[y][x] = Cell(x, y)

    def get_cell_by_pos(self, pos) -> Cell:
        return self.map[pos.y][pos.x]

    def get_cell(self, x, y) -> Cell:
        return self.map[y][x]

    def _setResource(self, r_type, x, y, amount):
        """
        do not use this function, this is for internal tracking of state
        """
        cell = self.get_cell(x, y)
        cell.resource = Resource(r_type, amount)

    def get_path_direction(
        self,
        start_pos: "Position",
        end_pos: "Position",
        allow_player_cities: bool = False,
        unit_positions: Optional[List["Position"]] = None,
    ) -> Optional[DIRECTIONS]:

        # TODO: add options to allow player cities
        # TODO: make sure oponent's cities are always masked
        # TODO: make sure to mask future positions of units

        matrix = game_map_to_array(self, start_pos, end_pos)
        path = bfs(matrix, (start_pos.x, start_pos.y))

        if path is None or len(path) < 2:
            return None

        x, y = path[1]
        next_pos = Position(x, y)
        disp = next_pos - start_pos
        direction = DIRECTIONS.get_from_coord(disp.x, disp.y)
        return direction

    def is_valid_position(self, pos: "Position") -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def get_plus_neighbors(self, pos: "Position") -> List["Position"]:
        pos_list: List[Position] = []
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            check_pos = pos + Position(x, y)
            if self.is_valid_position(check_pos):
                cell: Cell = self.get_cell_by_pos(check_pos)
                if not cell.has_resource() and cell.citytile is None:
                    pos_list.append(check_pos)
        return pos_list

    def __getitem__(self, key: Union["Position", Tuple[int, int]]) -> Cell:
        if type(key) is Position:
            return self.get_cell_by_pos(key)

        if isinstance(key, tuple) and list(map(type, key)) == [int, int]:
            return self.get_cell(key[0], key[1])

        raise ValueError("key must be of type Position or Tuple(int, int)")
