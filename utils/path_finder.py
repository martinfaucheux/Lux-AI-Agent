import collections
from typing import List, Tuple

import numpy as np

PathType = List[Tuple[int, int]]

WALL = 0
START = 1
END = 2
EMPTY = 3

def game_map_to_array(game_map, startPos, endPos) -> np.array:
    """Convert GameMap to an int array"""
    h = game_map.height
    w = game_map.width

    array = np.zeros((game_map.height, game_map.width))

    for y in range(h):
        for x in range(w):
            city_tile = game_map.get_cell(x, y).citytile
            array[y][x] = EMPTY if city_tile is None else WALL

    array[startPos.y][startPos.x] = START
    array[endPos.y][endPos.x] = END
    return array


def get_start_pos(grid):
    h = len(grid)
    w = len(grid[0])

    for i in range(h):
        for j in range(w):

            # If matrix[i][j] is source
            # and it is not visited
            if grid[i][j] == START:
                return i, j
    return -1, -1


def bfs(grid, start):

    # i, j = get_start_pos()

    height = len(grid)
    width = len(grid[0])
    queue = collections.deque([[start]])
    seen = set([start])

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == END:
            return path
        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (
                0 <= x2 < width
                and 0 <= y2 < height
                and grid[y2][x2] not in [START, WALL]
                and (x2, y2) not in seen
            ):
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


