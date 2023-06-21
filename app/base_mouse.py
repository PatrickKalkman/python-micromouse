import json
import pygame

from loguru import logger

from micro_mouse_colors import MicroMouseColor


class BaseMouse:
    MOVES = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    def __init__(self, position, goal, maze, exploring, view_distance=2):
        self.position = position
        self.start_postion = position
        self.goal = goal
        self.view_distance = view_distance
        self.maze = maze
        self.direction = (0, -1)
        self.exploring = exploring
        self.walls = set()
        self.visited = set()

    def look(self):
        surroundings = {}

        for direction, (dx, dy) in BaseMouse.MOVES.items():
            x, y = self.position[0] + dx * self.view_distance, self.position[1] + dy * self.view_distance

            if 0 <= x < self.maze.size and 0 <= y < self.maze.size:
                if self.exploring:
                    surroundings[direction] = self.maze.get(x, y)
                else:
                    cell_value = 0 if (x, y) in self.visited else 1
                    surroundings[direction] = cell_value

        return surroundings

    def save_exploration_data(self, filename='./mouse_exploration/exploration_data.json'):
        data = {
            'visited': list(self.visited),
            'walls': list(self.walls),
            'maze_size': self.maze.size,
            'goal': self.goal,
            'start': self.start_postion
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_exploration_data(self, filename='./mouse_exploration/exploration_data.json'):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.visited = set(tuple(pos) for pos in data['visited'])
        self.visited.add((27, 27))
        self.walls = set(tuple(pos) for pos in data['walls'])
        self.goal = tuple(data['goal'])
        self.position = tuple(data['start'])
        # Assuming the maze size doesn't change
        if self.maze.size != data['maze_size']:
            print("Warning: loaded maze size doesn't match current maze size.")

    def at_goal(self):
        return self.position == self.goal

    def move(self, direction):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

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
