import pygame
from loguru import logger

from micro_mouse_colors import MicroMouseColor

MOVE_MOUSE_EVENT = pygame.USEREVENT + 1


class MazeEventLoop:
    def __init__(self, maze, cell_size, mouse):
        self.cell_size = cell_size
        self.maze = maze
        self.mouse = mouse
        self.screen = self._initialize_screen(cell_size)
        pygame.time.set_timer(MOVE_MOUSE_EVENT, 70)

    def _initialize_screen(self, cell_size):
        screen_size = self.maze.size * cell_size
        screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Maze")
        return screen

    def _render_game(self):
        self.screen.fill(MicroMouseColor.BLACK)
        self.maze.draw(self.screen)
        self.mouse.draw(self.screen, self.cell_size)
        pygame.display.flip()

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == MOVE_MOUSE_EVENT:
            if not self.mouse.at_goal():
                self.mouse.step()
                self.maze.add_to_visited_cells(self.mouse.position)
            else:
                self._handle_goal_reached()
                return False
        return True

    def _handle_goal_reached(self):
        end_time = pygame.time.get_ticks()
        elapsed_time = end_time - self.start_time
        logger.info(f"Mouse reached the goal in {elapsed_time} ms.")
        pygame.time.set_timer(MOVE_MOUSE_EVENT, 0)
        self.mouse.save_exploration_data()

    def render_and_handle_events(self):
        running = True
        self.start_time = pygame.time.get_ticks()
        while running:
            self._render_game()
            for event in pygame.event.get():
                running = self._handle_event(event)
        pygame.quit()
