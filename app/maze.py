import numpy as np
import random
import pygame

from micro_mouse_colors import MicroMouseColor


class Maze:
    def __init__(self, size, start, end, seed=0):
        self.cells = []
        self.visited_cells = set()
        self.size = size
        self.start = start
        self.end = end
        self.grid = self._create_empty_grid()
        self._create_cells()
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

    def _color_for_cell(self, row, column):
        if self.get(row, column) == 1:  # wall cell
            return MicroMouseColor.BLACK
        elif (row, column) in self.visited_cells:  # visited cell
            return MicroMouseColor.LIGHT_RED
        else:  # unvisited cell
            return MicroMouseColor.WHITE

    def _create_cells(self):
        for row in range(self.size):
            row_cells = []
            for column in range(self.size):
                cell_rect = pygame.Rect(column * self.size,
                                        row * self.size,
                                        self.size, self.size)
                row_cells.append(cell_rect)
            self.cells.append(row_cells)

    def add_to_visited_cells(self, position):
        self.visited_cells.add(position)

    def draw(self, screen):
        for row in range(self.size):
            for column in range(self.size):
                cell_color = self._color_for_cell(row, column)
                pygame.draw.rect(screen, cell_color, self.cells[row][column])

        pygame.draw.rect(screen, MicroMouseColor.GREEN,
                         self.cells[self.start[0]][self.start[1]])
        pygame.draw.rect(screen, MicroMouseColor.BLUE,
                         self.cells[self.end[0]][self.end[1]])
