import heapq
from collections import defaultdict

from loguru import logger

from base_mouse import BaseMouse


class BasicMouse(BaseMouse):
    def __init__(self, position, goal, maze, is_exploring=True, view_distance=1):
        super().__init__(position, goal, maze, is_exploring, view_distance)
        self.stack = []  # for depth-first search
        self.visited = set()  # to keep track of visited cells
        self.walls = set()
        self.path = []  # to manage the current path and allow backtracking
        self.shortest_path = []
        self.distances = defaultdict(lambda: float('inf'))
        self.predecessors = {}
        self.is_exploring = is_exploring
        self.step_counter = 0

    def move(self, direction):
        self.direction = direction
        self.path.append(self.position)  # add current position to path before moving
        self.position = self.add_direction_to_position(self.position, direction)

    def add_direction_to_position(self, position, direction):
        """Helper function to add a direction to a position."""
        return position[0] + direction[0], position[1] + direction[1]

    def step(self):
        # Check if current position is already the goal
        if self.at_goal():
            return

        if self.is_exploring:
            self.explore()
        else:
            self.step_counter += 1
            if self.shortest_path:
                new_position = self.shortest_path.pop(0)
                self.direction = (new_position[0] - self.position[0], new_position[1] - self.position[1])
                self.position = new_position

    def explore(self):
        self.visited.add(self.position)
        surroundings = self.inspect_surroundings()
        unvisited_directions = self.get_unvisited_directions(surroundings)

        if unvisited_directions:
            # move to an unvisited cell
            self.stack.append(self.position)
            self.move(unvisited_directions[0])
        elif self.stack:
            # backtrack to the last junction
            backtrack_position = self.stack.pop()
            self.direction = self.get_direction_from_positions(backtrack_position, self.position)
            self.position = self.path.pop()

    def get_unvisited_directions(self, surroundings):
        """Helper function to get unvisited directions."""
        unvisited_directions = []

        for direction, cell in surroundings.items():
            new_position = self.add_direction_to_position(self.position, BaseMouse.MOVES[direction])

            # Only consider directions leading to open spaces and not previously visited
            if cell == 1:  # if cell is a wall
                self.walls.add(new_position)
            if cell == 0 and new_position not in self.visited:
                unvisited_directions.append(BaseMouse.MOVES[direction])

        return unvisited_directions

    def get_direction_from_positions(self, pos1, pos2):
        """Helper function to get the direction from one position to another."""
        return pos1[0] - pos2[0], pos1[1] - pos2[1]

    def run_dijkstra(self):
        heap = [(0, self.position)]
        self.distances[self.position] = 0
        visited = set()

        while heap:
            (dist, current) = heapq.heappop(heap)

            if current in visited:
                continue

            visited.add(current)

            if current == self.goal:  # stop when the goal is found
                break

            if dist != self.distances[current]:
                continue

            surroundings = self.inspect_surroundings()
            for direction, cell in surroundings.items():
                new_position = (current[0] + BaseMouse.MOVES[direction][0], current[1]
                                + BaseMouse.MOVES[direction][1])
                # only consider cells that are in the visited set and are not walls
                if new_position in self.visited and new_position not in self.walls:
                    alt_dist = self.distances[current] + 1
                    if alt_dist < self.distances[new_position]:
                        self.distances[new_position] = alt_dist
                        self.predecessors[new_position] = current
                        heapq.heappush(heap, (alt_dist, new_position))

    def reconstruct_path(self):
        path = []
        current = self.goal
        while current != self.position:
            path.append(current)
            current = self.predecessors[current]
        self.shortest_path = path[::-1]
