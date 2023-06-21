import numpy as np
import random


class Maze:
    def __init__(self, size, seed=0):
        self.size = size
        self.grid = self._create_empty_grid()
        random.seed(seed)  # set the random seed

    def _create_empty_grid(self):
        return np.ones((self.size, self.size))

    def _valid_next_cell(self, next_cell):
        return (next_cell[0] > 0 and next_cell[0] < self.size - 1) and \
               (next_cell[1] > 0 and next_cell[1] < self.size - 1) and \
               self.grid[next_cell[0]][next_cell[1]] == 1

    def _carve_path(self, current_cell, next_cell, direction):
        self.grid[current_cell[0] + direction[0]][current_cell[1] + direction[1]] = 0
        self.grid[next_cell[0]][next_cell[1]] = 0

    def carve_maze(self, current_cell=(1, 1)):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        for direction in directions:
            next_cell = (current_cell[0] + direction[0]*2,
                         current_cell[1] + direction[1]*2)
            if self._valid_next_cell(next_cell):
                self._carve_path(current_cell, next_cell, direction)
                self.carve_maze(next_cell)

    def get(self, row, column):
        return self.grid[row][column]
