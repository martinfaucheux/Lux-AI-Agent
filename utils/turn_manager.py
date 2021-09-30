import math
import sys
from typing import List, Optional

from lux import annotate
from lux.constants import Constants
from lux.game import Game
from lux.game_constants import GAME_CONSTANTS
from lux.game_map import RESOURCE_TYPES, Cell
from lux.game_objects import Player, Unit

from utils.log import Logger
from utils.map import get_adjacent_cells, get_closest_cell
from utils.unit import has_enough_resource

DIRECTIONS = Constants.DIRECTIONS
game_state = None

_MAX_CITIES = 2


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

    def play_turn(self):
        actions = []
        # we iterate over all our units and do something with them
        for unit in self.player.units:
            if unit.is_worker() and unit.can_act():

                # NOTE: this part is custom
                if self.player.city_tile_count < _MAX_CITIES and has_enough_resource(
                    unit
                ):

                    # get position to build
                    if self.player.city_tile_count > 0:

                        # TODO: fix how we get this position: it is wrong
                        existing_city_pos = self.city_tiles[0].pos
                        possible_cells = get_adjacent_cells(
                            game_state.map, existing_city_pos
                        )
                        closest_cell = get_closest_cell(
                            game_state.map, unit, possible_cells
                        )

                        self.log(str(closest_cell.pos) + " (city found)")

                    else:
                        possible_cells = get_adjacent_cells(game_state.map, unit.pos)
                        closest_cell = get_closest_cell(
                            game_state.map, unit, possible_cells
                        )
                        self.log(str(closest_cell.pos) + " (no city found)")

                    # build if possible
                    if closest_cell.pos == unit.pos:
                        actions.append(unit.build_city())
                    # or walk toward it
                    else:
                        self.log("move to city " + str(closest_cell.pos))

                        actions.append(
                            unit.move(unit.pos.direction_to(closest_cell.pos))
                        )

                elif unit.get_cargo_space_left() > 0:

                    # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
                    closest_resource_tile = self.get_closest_resource_tile(unit)

                    if closest_resource_tile is not None:
                        actions.append(
                            unit.move(unit.pos.direction_to(closest_resource_tile.pos))
                        )
                else:
                    # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
                    if len(self.player.cities) > 0:
                        closest_city_tile = self.get_closest_city_tile(unit)
                        if closest_city_tile is not None:
                            move_dir = unit.pos.direction_to(closest_city_tile.pos)
                            actions.append(unit.move(move_dir))

        return actions

    def get_closest_resource_tile(self, unit: Unit) -> Optional[Cell]:
        # TODO: use get_closest_cell instead
        closest_dist = math.inf
        for resource_tile in self.resource_tiles:
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

    def log(self, message: str):
        with open("log.txt", "a") as f:
            message = f"Team {self.player.team}: {message}\n"
            f.write(message)
