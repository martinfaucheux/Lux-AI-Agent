import numpy as np

from utils.path_finder import bfs, get_path

if __name__ == "__main__":

    matrix_list = [
        [
            [0, 3, 0, 1, 3],
            [3, 0, 3, 3, 3],
            [2, 3, 3, 3, 3],
            [0, 3, 3, 3, 3],
        ],
        [
            [0, 3, 0, 1, 3],
            [3, 0, 3, 3, 3],
            [2, 3, 3, 3, 0],
            [0, 3, 3, 0, 3],
        ],
        [
            [0, 3, 0, 1, 3],
            [3, 3, 3, 3, 3],
            [3, 3, 3, 2, 3],
            [0, 3, 3, 3, 3],
        ],
        [
            [0, 3, 0, 1],
            [0, 0, 3, 3],
            [2, 0, 3, 3],
            [0, 3, 3, 3],
        ],
    ]

    for matrix in matrix_list:

        matrix = np.array(matrix)

        # calling isPath method
        # res = get_path(matrix)
        start_pos = (3, 0)
        res = bfs(matrix, start_pos)

        print(res)
        print("\n\n\n\n")
