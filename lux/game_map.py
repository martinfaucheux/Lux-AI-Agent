import math
from typing import List, Optional, Tuple, Union

from utils.path_finder import bfs, game_map_to_array

from .constants import Constants

DIRECTIONS = Constants.DIRECTIONS
RESOURCE_TYPES = Constants.RESOURCE_TYPES


class Resource:
    def __init__(self, r_type: str, amount: int):
        self.type = r_type
        self.amount = amount


class Cell:
    def __init__(self, x, y):
        self.pos = Position(x, y)
        self.resource: Resource = None
        self.citytile = None
        self.road = 0

    def has_resource(self):
        return self.resource is not None and self.resource.amount > 0


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
        self, start_pos: "Position", end_pos: "Position"
    ) -> Optional[DIRECTIONS]:

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


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, pos) -> int:
        return abs(pos.x - self.x) + abs(pos.y - self.y)

    def distance_to(self, pos):
        """
        Returns Manhattan (L1/grid) distance to pos
        """
        diff = self - pos
        return math.sqrt(diff.x * diff.x + diff.y * diff.y)

    def is_adjacent(self, pos):
        return (self - pos) <= 1

    def __eq__(self, pos) -> bool:
        return self.x == pos.x and self.y == pos.y

    def equals(self, pos):
        return self == pos

    def translate(self, direction, units) -> "Position":
        if direction == DIRECTIONS.NORTH:
            return Position(self.x, self.y - units)
        elif direction == DIRECTIONS.EAST:
            return Position(self.x + units, self.y)
        elif direction == DIRECTIONS.SOUTH:
            return Position(self.x, self.y + units)
        elif direction == DIRECTIONS.WEST:
            return Position(self.x - units, self.y)
        elif direction == DIRECTIONS.CENTER:
            return Position(self.x, self.y)

    def direction_to(self, target_pos: "Position") -> DIRECTIONS:
        """
        Return closest position to target_pos from this position
        """
        check_dirs = [
            DIRECTIONS.NORTH,
            DIRECTIONS.EAST,
            DIRECTIONS.SOUTH,
            DIRECTIONS.WEST,
        ]
        closest_dist = self.distance_to(target_pos)
        closest_dir = DIRECTIONS.CENTER
        for direction in check_dirs:
            newpos = self.translate(direction, 1)
            dist = target_pos.distance_to(newpos)
            if dist < closest_dist:
                closest_dir = direction
                closest_dist = dist
        return closest_dir

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))
