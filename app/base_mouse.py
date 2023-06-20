class BaseMouse:
    MOVES = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    def __init__(self, position, goal, maze, view_distance=2):
        self.position = position
        self.goal = goal
        self.view_distance = view_distance
        self.maze = maze

    def look(self):
        surroundings = {}

        for direction, (dx, dy) in BaseMouse.MOVES.items():
            x, y = self.position[0] + dx * self.view_distance, self.position[1] + dy * self.view_distance

            if 0 <= x < self.maze.size and 0 <= y < self.maze.size:
                surroundings[direction] = self.maze.get(x, y)

        return surroundings

    def at_goal(self):
        return self.position == self.goal

    def move(self, direction):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError
