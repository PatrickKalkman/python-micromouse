import pygame
from loguru import logger

from base_mouse import BaseMouse
from micro_mouse_colors import MicroMouseColor


class BasicMouse(BaseMouse):
    def __init__(self, position, goal, maze, view_distance=1):
        super().__init__(position, goal, maze, view_distance)
        self.stack = []  # for depth-first search
        self.visited = set()  # to keep track of visited cells
        self.path = []  # to manage the current path and allow backtracking
        self.direction = (0, -1)

    def move(self, direction):
        self.direction = direction
        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        self.path.append(self.position)  # add current position to path before moving
        self.position = new_position

    def step(self):
        # first, check if current position is already the goal
        if self.at_goal():
            return

        self.visited.add(self.position)

        # get the surroundings
        surroundings = self.look()
        unvisited_directions = []

        for direction, cell in surroundings.items():
            new_position = (self.position[0] + BaseMouse.MOVES[direction][0],
                            self.position[1] + BaseMouse.MOVES[direction][1])

            # Only consider directions leading to open spaces and not previously visited
            if cell == 0 and new_position not in self.visited:
                unvisited_directions.append(BaseMouse.MOVES[direction])

        if unvisited_directions:
            # move to an unvisited cell
            self.stack.append(self.position)
            self.move(unvisited_directions[0])
        elif self.stack:
            # backtrack to the last junction
            backtrack_position = self.stack.pop()  # get the last junction from the stack
            # Update the direction when backtracking
            self.direction = (backtrack_position[0] - self.position[0],
                              backtrack_position[1] - self.position[1])

            while self.position != backtrack_position:
                if self.path:
                    self.position = self.path.pop()  # backtrack along the path
                else:
                    logger.error("Mouse trapped, no path to backtrack.")
                    return
        else:
            logger.error("Mouse trapped, no path to goal exists.")

    def draw(self, screen, cell_size):
        # calculate the points for the triangle
        x, y = self.position[1] * cell_size, self.position[0] * cell_size  # swap x and y
        if self.direction == (-1, 0):  # Up
            points = [(x, y + cell_size), (x + cell_size, y + cell_size), (x + cell_size / 2, y)]
        elif self.direction == (1, 0):  # Down
            points = [(x, y), (x + cell_size, y), (x + cell_size / 2, y + cell_size)]
        elif self.direction == (0, -1):  # Left
            points = [(x + cell_size, y), (x + cell_size, y + cell_size), (x, y + cell_size / 2)]
        else:  # Right
            points = [(x, y), (x, y + cell_size), (x + cell_size, y + cell_size / 2)]

        pygame.draw.polygon(screen, MicroMouseColor.RED, points)
