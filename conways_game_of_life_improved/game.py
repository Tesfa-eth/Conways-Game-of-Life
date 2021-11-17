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
from time import sleep
from numpy.core.defchararray import array
import pygame
import numpy as np

from create_grids import starting_array, add_Glider, add_Blinker, add_beacon, random_array

from button import Button 

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

def update_grid(array, block_size, start_update):
    """updates the grid and returns the new state"""
    newState = np.zeros((array.shape[0], array.shape[1]))
    # for now
    newState = array
    row, column = array.shape[0], array.shape[1]
    for i, j in np.ndindex(row-1, column-1):
        #if start_update:
        if start_update:
            newState[i,j] = check_rule(array, i, j)
        col = BLUE if newState[i, j] == 1 else WHITE
        rect = pygame.Rect(j*block_size, i*block_size, block_size-1, block_size-1)
        pygame.draw.rect(SCREEN, col, rect)

    return newState

def customize(mouse_position, grid):
    block_size = WINDOW_HEIGHT//grid.shape[0]
    i = mouse_position[0]//block_size
    j = mouse_position[1]//block_size
    grid[j][i] = 1
    #print(grid)
    return grid
    #print(i,j)
    #print(mouse_position[0]//block_size, mouse_position[1]//block_size)
    

def start_game(grid):
    """starts the game"""
    global SCREEN, CLOCK

    pygame.init()
    pygame.display.set_caption("Conways game of life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    
    
    
    #Termination Button 
    pause_button = Button('blue', 305, 500, 85, 50, 'Pause') #create quit button
    #stop_button.draw_rect(SCREEN) 
    
    #Pause Button 
    resume_button = Button('green', 400, 500, 110, 50, 'Resume')
    
    #Restart Button
    # color, x, y, width, height
    restart_button = Button('red', 180, 500, 110, 50, 'Restart')

    #Quit
    quit_button = Button('brown', 60, 500, 110, 50, 'Quit')

    #Start
    start_button = Button('black', 60, 430, 110, 50, 'Start')


    #Random start
    random_button = Button('brown', WINDOW_HEIGHT//2, WINDOW_WIDTH/2, 190, 90, 'Random Start')
    
    #Glider
    customize_button = Button('brown',WINDOW_WIDTH/2-250, WINDOW_HEIGHT//2, 190, 90, 'Customize')
    
    import time
    pause = False
    start = False
    update = False
    custom = False
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if custom: # clicked user input
                        grid = customize(mouse_position, grid)
                    if resume_button.mouse_over(mouse_position):
                        pause = False
                    if pause_button.mouse_over(mouse_position):
                        pause = True
                    if restart_button.mouse_over(mouse_position):
                        main()

                    if start_button.mouse_over(mouse_position):
                        #start update
                        update = True
                        custom = False
                        #main()
                    if random_button.mouse_over(mouse_position):
                        start = True
                    if customize_button.mouse_over(mouse_position):
                        array_start = starting_array((40,40))
                        custom = True
                        #add_Glider(array_start.shape[0]//2 -2,array_start.shape[0]//2 -2, array_start)
                        grid = array_start
                        start = True
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.mouse_over(mouse_position):
                        pygame.quit()

        # get mouse position              
        mouse_position = pygame.mouse.get_pos() # tuple of x, y coordinates 
        
        """if custom:
            grid = customize(mouse_position, grid)"""
            #print(mouse_position)
        # once starts
    
        if start:
            SCREEN.fill(BLUE)
            grid = update_grid(grid, WINDOW_HEIGHT//grid.shape[0], update) # has to be both height and width
            # draw buttons
            resume_button.draw_rect(SCREEN)
            pause_button.draw_rect(SCREEN)
            restart_button.draw_rect(SCREEN)
            quit_button.draw_rect(SCREEN)
            start_button.draw_rect(SCREEN)
        
        # before the game starts
        else:
            # menu here
            SCREEN.fill(BLUE)
            random_button.draw_rect(SCREEN)
            customize_button.draw_rect(SCREEN)

        print(grid)
        # update the grid unless it is paused
        if pause == False:
            pygame.display.update()


def main(begin=random_array(20, 20)):
    #array_start = starting_array((5,5))
    array_start = begin
    add_Blinker(array_start.shape[0]//2 -2,array_start.shape[0]//2 -2, array_start)
    #add_Glider(array_start.shape[0]//2 -2,array_start.shape[0]//2 -2, array_start)
    #add_beacon(array_start.shape[0]//2 -2,array_start.shape[0]//2 -2, array_start)

    start_game(array_start)


if __name__ == "__main__":
    main()