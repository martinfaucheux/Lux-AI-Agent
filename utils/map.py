import math
from typing import List, Optional, Set, Union

from lux.game_map import Cell, Position
from lux.game_objects import Unit


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
