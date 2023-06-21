import argparse
import pygame
from maze import Maze
from maze_event_loop import MazeEventLoop
from basic_mouse import BasicMouse


def main(seed, exploring):
    # Generate a complete maze
    size = 29
    start = (1, 1)
    end = (size - 2, size - 2)
    maze = Maze(size, start, end, seed)
    maze.carve_maze()

    mouse = BasicMouse(start, end, maze, is_exploring=exploring)
    if not exploring:
        mouse.load_exploration_data()
        mouse.run_dijkstra()
        mouse.reconstruct_path()

    maze_event_loop = MazeEventLoop(maze, size, mouse)

    pygame.init()
    maze_event_loop.render_and_handle_events()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the micromouse simulation.')
    parser.add_argument('--seed', type=int, default=0,
                        help='Seed for random number generator. Default: 0')
    parser.add_argument('--exploring', action='store_true',
                        help='Load exploration data at start. Default: False')

    args = parser.parse_args()

    main(args.seed, args.exploring)
