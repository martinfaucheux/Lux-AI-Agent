import math
from typing import List, Optional, Set, Tuple, Union

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

    def get_cell_by_pos(self, pos: Position) -> Cell:
        return self.map[pos.y][pos.x]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.map[y][x]

    def _setResource(self, r_type, x, y, amount):
        """
        do not use this function, this is for internal tracking of state
        """
        cell = self.get_cell(x, y)
        cell.resource = Resource(r_type, amount)

    def get_path_direction(
        self,
        start_pos: Position,
        end_pos: Position,
        allowed_city_teams: Optional[List[int]] = None,
        unit_positions: Optional[List[Position]] = None,
    ) -> Optional[DIRECTIONS]:

        allowed_city_teams: List[int] = allowed_city_teams or []
        forbidden_pos: Set[Position] = set()

        if unit_positions:
            forbidden_pos = set(unit_positions)

        for cell in self:
            if cell.citytile and cell.citytile.team not in allowed_city_teams:
                forbidden_pos.add(cell.pos)

        matrix = game_map_to_array(self, start_pos, end_pos, forbidden_pos)
        path = bfs(matrix, (start_pos.x, start_pos.y))

        if path is None or len(path) < 2:
            return DIRECTIONS.CENTER

        x, y = path[1]
        next_pos = Position(x, y)
        disp = next_pos - start_pos
        direction = DIRECTIONS.get_from_coord(disp.x, disp.y)
        return direction

    def is_valid_position(self, obj: Union[Position, Tuple[int, int]]) -> bool:
        x, y = self.get_tuple(obj)
        return 0 <= x < self.width and 0 <= y < self.height

    def get_plus_neighbors(self, pos: Position) -> List[Position]:
        pos_list: List[Position] = []
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            check_pos = pos + Position(x, y)
            if self.is_valid_position(check_pos):
                cell: Cell = self.get_cell_by_pos(check_pos)
                if not cell.has_resource() and cell.citytile is None:
                    pos_list.append(check_pos)
        return pos_list

    def __getitem__(self, key: Union[Position, Tuple[int, int]]) -> Cell:
        x, y = self.get_tuple(key)
        return self.get_cell(x, y)

    def __iter__(self) -> "GameMapIterator":
        return GameMapIterator(self)

    @staticmethod
    def get_tuple(obj: Union[Position, Tuple[int, int]]):
        if type(obj) is Position:
            return (obj.x, obj.y)

        if isinstance(obj, tuple) and list(map(type, obj)) == [int, int]:
            return obj

        raise ValueError("key must be of type Position or Tuple(int, int)")


class GameMapIterator(object):
    def __init__(self, game_map: GameMap):
        self.game_map = game_map
        self._x: int = 0
        self._y: int = 0

    def __next__(self) -> Cell:
        x, y = self._x, self._y
        if self.game_map.is_valid_position((x, y)):
            self.incr()
            return self.game_map[(x, y)]
        raise StopIteration

    def incr(self):
        if self._x == self.game_map.width - 1:
            self._x = 0
            self._y += 1
        else:
            self._x += 1
