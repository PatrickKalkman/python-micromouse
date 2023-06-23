import json
import pygame

from loguru import logger

from app.micro_mouse_colors import MicroMouseColor


class BaseMouse:
    MOVES = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    def __init__(self, position, goal, maze, exploring,
                 exploration_data_location, view_distance=2):
        self.position = position
        self.start_position = position
        self.goal = goal
        self.view_distance = view_distance
        self.maze = maze
        self.direction = (0, -1)
        self.exploring = exploring
        self.walls = set()
        self.visited = set()
        self.exploration_data_location = exploration_data_location

    def inspect_surroundings(self):
        surroundings = {}
        for direction, (dx, dy) in BaseMouse.MOVES.items():
            x, y = (self.position[0] + dx * self.view_distance,
                    self.position[1] + dy * self.view_distance)

            if 0 <= x < self.maze.size and 0 <= y < self.maze.size:
                surroundings[direction] = self._inspect_cell(x, y)

        return surroundings

    def _inspect_cell(self, x, y):
        if self.exploring:
            return self.maze.get(x, y)
        else:
            return 0 if (x, y) in self.visited else 1

    def load_exploration_data(self):
        with open(self.exploration_data_location, 'r') as f:
            data = json.load(f)
        self._update_mouse_data(data)

    def save_exploration_data(self):
        data = self._prepare_exploration_data()
        with open(self.exploration_data_location, 'w') as f:
            json.dump(data, f)

    def _prepare_exploration_data(self):
        return {
            'visited': list(self.visited),
            'walls': list(self.walls),
            'maze_size': self.maze.size,
            'goal': self.goal,
            'start': self.start_position
        }

    def _update_mouse_data(self, data):
        self.visited = set(tuple(pos) for pos in data['visited'])
        self.visited.add((27, 27))
        self.walls = set(tuple(pos) for pos in data['walls'])
        self.goal = tuple(data['goal'])
        self.position = tuple(data['start'])
        if self.maze.size != data['maze_size']:
            logger.warning("Loaded maze size doesn't match current maze size.")

    def at_goal(self):
        return self.position == self.goal

    def draw(self, screen, cell_size):
        x, y = self.position[1] * cell_size, self.position[0] * cell_size
        points = self._calculate_draw_points(x, y, cell_size)
        pygame.draw.polygon(screen, MicroMouseColor.RED, points)

    def _calculate_draw_points(self, x, y, cell_size):
        if self.direction == (-1, 0):  # Up
            return [(x, y + cell_size),
                    (x + cell_size, y + cell_size),
                    (x + cell_size / 2, y)]
        elif self.direction == (1, 0):  # Down
            return [(x, y),
                    (x + cell_size, y),
                    (x + cell_size / 2, y + cell_size)]
        elif self.direction == (0, -1):  # Left
            return [(x + cell_size, y),
                    (x + cell_size, y + cell_size),
                    (x, y + cell_size / 2)]
        else:  # Right
            return [(x, y),
                    (x, y + cell_size),
                    (x + cell_size, y + cell_size / 2)]

    def move(self, direction):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError
