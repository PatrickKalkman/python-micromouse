import heapq
from collections import defaultdict

from base_mouse import BaseMouse


class BasicMouse(BaseMouse):
    def __init__(self, position, goal, maze, exploration_data_location, is_exploring,
                 view_distance=1):
        super().__init__(position, goal, maze, is_exploring,
                         exploration_data_location, view_distance)
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
        if self.at_goal():
            return

        self.explore() if self.is_exploring else self.follow_shortest_path()

    def follow_shortest_path(self):
        self.step_counter += 1
        if self.shortest_path:
            self.move_along_shortest_path()

    def move_along_shortest_path(self):
        new_position = self.shortest_path.pop(0)
        self.direction = self.get_direction_from_positions(new_position, self.position)
        self.position = new_position

    def explore(self):
        self.visited.add(self.position)
        surroundings = self.inspect_surroundings()
        unvisited_directions = self.get_unvisited_directions(surroundings)

        if unvisited_directions:
            self.move_to_unvisited(unvisited_directions)
        elif self.stack:
            self.backtrack()

    def move_to_unvisited(self, unvisited_directions):
        # move to an unvisited cell
        self.stack.append(self.position)
        self.move(unvisited_directions[0])

    def backtrack(self):
        # backtrack to the last junction
        backtrack_position = self.stack.pop()
        self.direction = self.get_direction_from_positions(backtrack_position,
                                                           self.position)
        self.position = self.path.pop()

    def get_unvisited_directions(self, surroundings):
        """Helper function to get unvisited directions."""
        unvisited_directions = []

        for direction, cell in surroundings.items():
            new_position = self.add_direction_to_position(self.position,
                                                          BaseMouse.MOVES[direction])

            # Only consider directions leading to open spaces and not previously visited
            if cell == 1:  # if cell is a wall
                self.walls.add(new_position)
            if cell == 0 and new_position not in self.visited:
                unvisited_directions.append(BaseMouse.MOVES[direction])

        return unvisited_directions

    def get_direction_from_positions(self, pos1, pos2):
        return pos1[0] - pos2[0], pos1[1] - pos2[1]

    def run_dijkstra(self):
        heap = [(0, self.position)]
        self.distances[self.position] = 0
        visited = set()

        while heap:
            dist, current = heapq.heappop(heap)

            if self.is_visited_or_distance_changed(current, visited, dist):
                continue

            visited.add(current)

            if current == self.goal:  # stop when the goal is found
                break

            self.update_distances_and_predecessors(heap, current)

    def is_visited_or_distance_changed(self, current, visited, dist):
        return current in visited or dist != self.distances[current]

    def update_distances_and_predecessors(self, heap, current):
        surroundings = self.inspect_surroundings()
        for direction, cell in surroundings.items():
            new_position = self.add_direction_to_position(current,
                                                          BaseMouse.MOVES[direction])

            # only consider cells that are in the visited set and are not walls
            if self.is_valid_position(new_position):
                self.update_distance_and_predecessor(heap, current, new_position)

    def is_valid_position(self, position):
        return position in self.visited and position not in self.walls

    def update_distance_and_predecessor(self, heap, current, new_position):
        alt_dist = self.distances[current] + 1
        if alt_dist < self.distances[new_position]:
            self.distances[new_position] = alt_dist
            self.predecessors[new_position] = current
            heapq.heappush(heap, (alt_dist, new_position))

    def reconstruct_path(self):
        self.shortest_path = self.construct_path_from_predecessors()[::-1]

    def construct_path_from_predecessors(self):
        path = []
        current = self.goal
        while current != self.position:
            path.append(current)
            current = self.predecessors[current]
        return path
