import pygame
from maze import Maze
from maze_display import MazeDisplay
from basic_mouse import BasicMouse

# Generate a complete maze
size = 29
start = (1, 1)
end = (size - 2, size - 2)
maze = Maze(size)
maze.carve_maze()
mouse = BasicMouse(start, end, maze)
mazeDisplay = MazeDisplay(maze, start, end, size, mouse)

# Initialize Pygame
pygame.init()
mazeDisplay.draw()
