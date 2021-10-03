import collections
from typing import List, Tuple

import numpy as np

PathType = List[Tuple[int, int]]

WALL = 0
START = 1
END = 2
EMPTY = 3


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


# Method for finding and printing
# whether the path exists or not
def get_path(matrix: np.array) -> PathType:

    h, w = matrix.shape

    # Defining visited array to keep
    # track of already visited indexes

    visited = np.zeros((h, w))
    # visited = [[False for x in range(n)] for y in range(n)]

    # Flag to indicate whether the
    # path exists or not
    result = False, None

    for i in range(h):
        for j in range(w):

            # If matrix[i][j] is source
            # and it is not visited
            if matrix[i][j] == START and not visited[i][j]:

                # Starting from i, j and
                # then finding the path
                result, path = get_path_rec(matrix, i, j, visited, [])
                if result:
                    break
    return path


# Method for checking boundaries
def is_valid_position(i, j, matrix) -> bool:
    return i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0])


# Returns true if there is a
# path from a source(a
# cell with value 1) to a
# destination(a cell with
# value 2)
def get_path_rec(
    matrix: np.array, i: int, j: int, visited: np.array, path: List[Tuple[int, int]]
):

    # Checking the boundaries, walls and
    # whether the cell is unvisited
    if is_valid_position(i, j, matrix) and matrix[i][j] != WALL and not visited[i][j]:

        # If the cell is the required
        # destination then return true
        if matrix[i][j] == END:
            return True, path

        # Make the cell visited
        visited[i][j] = True

        shortest_path = None
        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            res, sub_path = get_path_rec(
                matrix, i + di, j + dj, visited, path + [(i + di, j + dj)]
            )
            if res:
                if (shortest_path is None) or (len(sub_path) < len(shortest_path)):
                    shortest_path = sub_path

        if shortest_path is not None:
            return True, shortest_path

    # No path has been found
    return False, None
