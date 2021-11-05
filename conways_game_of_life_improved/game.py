"""
Play the game according to the rules
Draw a window using pygame

Two issues that should be corrected:
 - what happens when the cell hits the wall. Currently,
  it stops
 - This has slightly disrupted the size of the window creating some
 black edge.
"""

from os import name
from numpy.core.defchararray import array
import pygame
import numpy as np

from create_grids import starting_array, add_Glider, add_Blinker, add_beacon, random_array

BLUE = (34, 36, 128)
WHITE = (200,200,200)
BLACK = (0,0,0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
col = WHITE
padding = 6

def get_neighbours(array, i, j):
    """returns all the 8 neighbours of a cell"""
    return (array[i-1, j-1], array[i-1, j], array[i-1,j+1], array[i, j-1], array[i, j+1], 
        array[i+1, j-1], array[i+1, j], array[i+1, j+1])

def is_padding(cell, padding):
    """
    checks if a cell is a padding. Meaning, checks if the 'cell' is an actuall cell 
    or a wall.
    return: bool
    """
    return cell == padding


def remove_edges(neighbours, padding=padding):
    """takes in a tuple and removes the egdes from them"""
    neighbours_list = list(neighbours)
    egdeless_neighbours = [ 0 if is_padding(x, padding) else int(x) for x in neighbours_list]
    return tuple(egdeless_neighbours)

def is_alive(cell):
    """returs True if a cell is alive and false, otherwise."""
    return True if cell == 1 else False

def check_rule(array,i, j):
    """
    cell - the cell it self
    i,j - the location of the cell in the grid
    return: 0 (if it will die) or 1 (if it will live)
    """
    neighbours = get_neighbours(array, i, j)
    actual_neighbours = remove_edges(neighbours)
    neighbour_value = sum(list(actual_neighbours))

    if is_alive(array[i,j]):
        if neighbour_value == 2 or neighbour_value == 3:
            return 1
        else:
            return 0

    else:
        if neighbour_value == 3:
            return 1
        else:
            return 0

def update_grid(array, block_size):
    """updates the grid and returns the new state"""
    newState = np.zeros((array.shape[0], array.shape[1]))
    row, column = array.shape[0], array.shape[1]

    for i, j in np.ndindex(row-1, column-1):
        newState[i,j] = check_rule(array, i, j)
        col = BLUE if newState[i, j] == 1 else WHITE
        rect = pygame.Rect(j*block_size, i*block_size, block_size-1, block_size-1)
        pygame.draw.rect(SCREEN, col, rect)

    return newState

def start_game(grid):
    """starts the game"""
    global SCREEN, CLOCK

    pygame.init()
    pygame.display.set_caption("Conways game of life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    import time
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        time.sleep(0.5)
        grid = update_grid(grid, WINDOW_HEIGHT//grid.shape[0]) # has to be both height and width
        pygame.display.update()


def main():
    #array_start = starting_array((20,20))
    array_start = random_array(40,40)
    #add_Blinker(array_start.shape[0]//2 -2,array_start.shape[0]//2 -2, array_start)
    #add_Glider(array_start.shape[0]//2 -2,array_start.shape[0]//2 -2, array_start)
    #add_beacon(array_start.shape[0]//2 -2,array_start.shape[0]//2 -2, array_start)

    start_game(array_start)


if __name__ == "__main__":
    main()