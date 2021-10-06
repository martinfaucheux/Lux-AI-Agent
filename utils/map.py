import math
from typing import List, Optional, Set, Union

from lux.game_map import Cell, GameMap, Position
from lux.game_objects import Unit


def get_adjacent_cells(
    game_map: GameMap,
    position: Position,
    allow_city: bool = False,
    allow_resource: bool = False,
):
    cells: List[Cell] = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            test_position = position + Position(x, y)
            if game_map.is_valid_position(test_position):
                cell = game_map.get_cell_by_pos(test_position)
                if cell.citytile and not allow_city:
                    continue
                if cell.resource and not allow_resource:
                    continue
                cells.append(cell)

    return cells


def get_closest_cell(
    obj: Union[Unit, Position, Cell], possible_cells: Union[List[Cell], Set[Cell]]
) -> Optional[Cell]:
    closest_dist = math.inf
    closest_cell = None

    pos: Position
    if type(obj) in [Unit, Cell]:
        pos = obj.pos
    else:
        pos = obj

    for possible_cell in possible_cells:
        dist = possible_cell.pos.distance_to(pos)
        if dist < closest_dist:
            closest_dist = dist
            closest_cell = possible_cell

    return closest_cell
