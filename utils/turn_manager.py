import math
from typing import Dict, List, Optional, Set

from lux import annotate
from lux.constants import Constants
from lux.game import Game
from lux.game_map import Cell, GameMap, Position
from lux.game_objects import Unit

from utils.map import get_closest_cell

DIRECTIONS = Constants.DIRECTIONS
game_state = None

unit_objectives = {}

_DEFAULT_MAX_CITIES = 3
_DEFAULT_MAX_UNITS = 2


class TurnManager:
    def __init__(self, observation, configuration):
        global game_state

        ### Do not edit ###
        if observation["step"] == 0:
            game_state = Game()
            game_state._initialize(observation["updates"])
            game_state._update(observation["updates"][2:])
            game_state.id = observation.player
        else:
            game_state._update(observation["updates"])

        ### AI Code goes down here! ###
        self.player = game_state.players[observation.player]
        self.opponent = game_state.players[(observation.player + 1) % 2]

        self._resource_tiles = None
        self._city_tiles = None

        configuration = configuration or {}
        self.max_cities = configuration.get("MAX_CITIES", _DEFAULT_MAX_CITIES)
        self.max_units = configuration.get("MAX_UNITS", _DEFAULT_MAX_UNITS)

        self.unit_count_forcast = len(self.player.units)
        self.citytile_count_forcast = self.player.city_tile_count

        self.future_unit_pos: Dict[Unit, Position] = {
            unit: unit.pos for unit in self.player.units
        }

    def play_turn(self):
        actions = []
        # we iterate over all our units and do something with them
        for unit in self.player.units:

            objective_position = self.get_objective(unit)

            if unit.is_worker() and unit.can_act():

                if (
                    objective_position is None
                    and self.citytile_count_forcast < self.max_cities
                    and unit.has_enough_resource()
                ):
                    # get new objective for the unit
                    closest_cell = self.get_next_city_cell(unit.pos)
                    self.set_objective(unit, closest_cell.pos)
                    objective_position = closest_cell.pos

                if (
                    objective_position is not None
                    and self.citytile_count_forcast < self.max_cities
                    and unit.has_enough_resource()
                ):
                    # signal that this unit will build
                    self.citytile_count_forcast += 1

                    actions.append(
                        annotate.circle(objective_position.x, objective_position.y)
                    )

                    # build if possible
                    if objective_position == unit.pos:
                        actions.append(unit.build_city())
                        self.clear_objective(unit)
                    # or walk toward it
                    else:
                        actions += self.get_path_direction(unit, objective_position)

                elif unit.get_cargo_space_left() > 0:

                    # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
                    closest_resource_tile = self.get_closest_resource_tile(unit)

                    if closest_resource_tile is not None:
                        actions += self.get_path_direction(
                            unit, closest_resource_tile.pos
                        )
                else:
                    # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
                    if len(self.player.cities) > 0:

                        # closest_city_tile = self.get_closest_city_tile(unit)
                        closest_city_tile = self.get_closest_poorest_city_tile(unit)

                        if closest_city_tile is not None:
                            actions += self.get_path_direction(
                                unit, closest_city_tile.pos
                            )

        for _, city in self.player.cities.items():
            for city_tile in city.citytiles:
                if city_tile.cooldown < 1:
                    if (
                        self.player.city_tile_count > len(self.player.units)
                        and self.unit_count_forcast < self.max_units
                    ):
                        actions.append(city_tile.build_worker())
                        self.unit_count_forcast += 1
                    # TODO: else research
        return actions

    def get_closest_resource_tile(self, unit: Unit) -> Optional[Cell]:
        closest_dist = math.inf
        for resource_tile in self.resource_tiles:
            pos = resource_tile.pos
            if (
                resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL
                and not self.player.researched_coal()
            ):
                continue
            if (
                resource_tile.resource.type == Constants.RESOURCE_TYPES.URANIUM
                and not self.player.researched_uranium()
            ):
                continue
            if pos != unit.pos and pos in list(self.future_unit_pos.values()):
                continue

            dist = resource_tile.pos.distance_to(unit.pos)
            if dist < closest_dist:
                closest_dist = dist
                closest_resource_tile = resource_tile

        return closest_resource_tile

    def get_closest_city_tile(self, unit: Unit):
        # TODO: use get_closest_cell instead
        closest_dist = math.inf
        closest_city_tile = None
        for k, city in self.player.cities.items():
            for city_tile in city.citytiles:
                dist = city_tile.pos.distance_to(unit.pos)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_city_tile = city_tile

        return closest_city_tile

    def get_poorest_city(self):
        cities = sorted(list(self.player.cities.values()), key=lambda city: city.fuel)
        return cities[0] if cities else None

    def get_closest_poorest_city_tile(self, unit: Unit) -> Cell:
        poorest_city = self.get_poorest_city()

        if poorest_city is None:
            return None

        possible_cells = [
            game_state.map.get_cell_by_pos(city_tile.pos)
            for city_tile in poorest_city.citytiles
        ]

        return get_closest_cell(unit, possible_cells)

    def get_next_city_cell(self, pos: Position) -> Optional[Cell]:

        possible_cells: Set[Cell] = set()
        for cell in self.city_tiles:
            pos_list = self.map.get_plus_neighbors(cell.pos)
            for pos in pos_list:
                possible_cells.add(self.map[pos])

        if possible_cells:
            return get_closest_cell(pos, possible_cells)

        # if no possible cell, return first ad
        possible_cells = [
            self.map.get_cell_by_pos(pos) for pos in self.map.get_plus_neighbors(pos)
        ]

        if possible_cells:
            return possible_cells[0]

        return None

    def get_path_direction(
        self, unit: Unit, target_pos: Position, allow_own_city: bool = False
    ):
        actions = []
        allowed_teams = [self.player.team] if allow_own_city else []
        # TODO: remove units on cities if cities are accepted
        direction = game_state.map.get_path_direction(
            unit.pos,
            target_pos,
            allowed_city_teams=allowed_teams,
            unit_positions=list(self.future_unit_pos.values()),
        )
        actions.append(unit.move(direction))
        self.future_unit_pos[unit] = unit.pos.translate(direction)
        return actions

    @property
    def map(self) -> GameMap:
        return game_state.map

    @property
    def width(self) -> int:
        return game_state.map.width

    @property
    def height(self) -> int:
        return game_state.map.height

    @property
    def resource_tiles(self) -> List[Cell]:
        if self._resource_tiles is None:
            self._resource_tiles = []
            for y in range(self.height):
                for x in range(self.width):
                    cell = game_state.map.get_cell(x, y)
                    if cell.has_resource():
                        self.resource_tiles.append(cell)

        return self._resource_tiles

    @property
    def city_tiles(self) -> List[Cell]:
        # TODO: cache this instead

        res = []
        for y in range(self.height):
            for x in range(self.width):
                cell = game_state.map.get_cell(x, y)
                city_tile = cell.citytile
                if city_tile is not None and city_tile.team == self.player.team:
                    res.append(cell)
        return res

    def get_objective(self, unit: Unit) -> Position:
        return unit_objectives.get(unit)

    def clear_objective(self, unit: Unit) -> None:
        del unit_objectives[unit]

    def set_objective(self, unit: Unit, position: Position) -> None:
        unit_objectives[unit] = position

    def log(self, message: str):
        if self.player.team != 0:
            return

        with open("log.txt", "a") as f:
            message = f"[Turn {game_state.turn}]Team {self.player.team}: {message}\n"
            f.write(message)
