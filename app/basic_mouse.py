from loguru import logger
from base_mouse import BaseMouse


class BasicMouse(BaseMouse):
    def get_surroundings(self, maze):
        return self.look(maze)

    def move(self, direction):
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])

    def step(self):
        logger.info("BasicMouse.step() not implemented")
