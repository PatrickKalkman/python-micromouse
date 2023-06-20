import pygame

MOVE_MOUSE_EVENT = pygame.USEREVENT + 1


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)


class MazeDisplay:
    def __init__(self, maze, start, end, cell_size, mouse):
        self.maze = maze
        self.start = start
        self.end = end
        self.cell_size = cell_size
        self.cells = self._create_cells()
        self.screen = self._create_screen()
        self.mouse = mouse
        pygame.time.set_timer(MOVE_MOUSE_EVENT, 1000)  # trigger every 1000 milliseconds

    def _create_cells(self):
        cells = []
        for row in range(self.maze.size):
            row_cells = []
            for column in range(self.maze.size):
                cell_rect = pygame.Rect(column * self.cell_size,
                                        row * self.cell_size,
                                        self.cell_size, self.cell_size)
                row_cells.append(cell_rect)
            cells.append(row_cells)
        return cells

    def _create_screen(self):
        screen_size = self.maze.size * self.cell_size
        screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Maze")
        return screen

    def _color_for_cell(self, row, column):
        if self.maze.get(row, column) == 0:
            return Color.WHITE
        else:
            return Color.BLACK

    def draw(self):
        running = True
        while running:
            self.screen.fill(Color.BLACK)

            for row in range(self.maze.size):
                for column in range(self.maze.size):
                    cell_color = self._color_for_cell(row, column)
                    pygame.draw.rect(self.screen, cell_color, self.cells[row][column])

            pygame.draw.rect(self.screen, Color.GREEN,
                             self.cells[self.start[0]][self.start[1]])
            pygame.draw.rect(self.screen, Color.BLUE,
                             self.cells[self.end[0]][self.end[1]])

            pygame.draw.rect(self.screen, Color.RED,
                             self.cells[self.mouse.position[0]][self.mouse.position[1]])

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == MOVE_MOUSE_EVENT:
                    if not self.mouse.at_goal():
                        self.mouse.step()
                    else:
                        pygame.time.set_timer(MOVE_MOUSE_EVENT, 0)  # stop the timer

        pygame.quit()
