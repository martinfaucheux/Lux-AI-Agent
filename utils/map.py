import math
from typing import List

from lux.game_map import Cell, GameMap, Position
from lux.game_objects import Unit


def is_valid_position(game_map: GameMap, position: Position) -> bool:
    return (
        position.x >= 0
        and position.x < game_map.width
        and position.y >= 0
        and position.y < game_map.height
    )


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
            if is_valid_position(game_map, test_position):
                cell = game_map.get_cell_by_pos(test_position)
                if cell.citytile and not allow_city:
                    continue
                if cell.resource and not allow_resource:
                    continue
                cells.append(cell)

    return cells


def get_closest_cell(game_map: GameMap, unit: Unit, possible_cells: List[Cell]):
    closest_dist = math.inf
    for possible_cell in possible_cells:
        dist = possible_cell.pos.distance_to(unit.pos)
        if dist < closest_dist:
            closest_dist = dist
            closest_cell = possible_cell

    return closest_cell
