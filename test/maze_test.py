import pytest
from app.maze import Maze


def test_create_empty_grid():
    maze = Maze(10)
    assert maze.grid.shape == (10, 10)
    assert (maze.grid == 1).all()  # All elements should be 1


def test_valid_next_cell():
    maze = Maze(10)
    assert maze._valid_next_cell((1, 1))  # Inside the maze
    assert not maze._valid_next_cell((0, 0))  # On the edge of the maze
    assert not maze._valid_next_cell((-1, -1))  # Outside the maze
    assert not maze._valid_next_cell((10, 10))  # Outside the maze
    assert not maze._valid_next_cell((11, 11))  # Outside the maze

    maze.grid[5][5] = 0
    assert not maze._valid_next_cell((5, 5))  # Cell is already 0


def test_get():
    maze = Maze(10)
    assert maze.get(0, 0) == 1
    maze.grid[0][0] = 0
    assert maze.get(0, 0) == 0
    with pytest.raises(IndexError):
        maze.get(10, 10)  # Outside the maze


def test_carve_maze():
    maze = Maze(10)
    maze.carve_maze()
    assert (maze.grid == 1).sum() > 0  # Some cells should still be 1 (walls)
    assert (maze.grid == 0).sum() > 0  # Some cells should be 0 (paths)
