class BaseMouse:
    def __init__(self, position, goal, view_distance=2):
        self.position = position
        self.goal = goal
        self.view_distance = view_distance

    def look(self, maze):
        surrounding = {}
        for dx in range(-self.view_distance, self.view_distance + 1):
            for dy in range(-self.view_distance, self.view_distance + 1):
                x, y = self.position[0] + dx, self.position[1] + dy
                if 0 <= x < maze.size and 0 <= y < maze.size:
                    surrounding[(dx, dy)] = maze.get(x, y)
        return surrounding

    def at_goal(self):
        return self.position == self.goal

    def move(self, direction):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError
