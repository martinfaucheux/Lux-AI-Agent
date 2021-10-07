import math
from typing import Dict, List, Optional, Tuple, Union

from utils.path_finder import bfs, game_map_to_array

from ..constants import Constants

DIRECTIONS = Constants.DIRECTIONS
RESOURCE_TYPES = Constants.RESOURCE_TYPES


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, pos) -> int:
        return abs(pos.x - self.x) + abs(pos.y - self.y)

    def distance_to(self, pos) -> float:
        """
        Returns Manhattan (L1/grid) distance to pos
        """
        diff = self - pos
        return math.sqrt(diff.x * diff.x + diff.y * diff.y)

    def is_adjacent(self, pos) -> bool:
        # TODO: check this, might not work properly
        return (self - pos) <= 1

    def __eq__(self, pos) -> bool:
        return self.x == pos.x and self.y == pos.y

    def equals(self, pos):
        return self == pos

    def translate(self, direction, units=1) -> "Position":
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
