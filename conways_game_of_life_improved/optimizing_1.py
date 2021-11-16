'''
Optimizing the calculation for each frame
'''
from os import name
from numpy.core.defchararray import array
import pygame
import numpy as np

from create_grids import random_array, add_Glider,  starting_array

BLUE = (34, 36, 128)
WHITE = (200,200,200)
BLACK = (0,0,0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
col = WHITE
arr = starting_array((10,10))
add_Glider(0,0,arr)

def array_(array, index_):
    """gives the value of the cell meaning 0 or 1. Takes in a tumple of (row, column)"""
    return array[index_[0], index_[1]]




def neighbours_(array, index_):
    """calculates the number of living neighbors"""
    i = index_[0]
    j = index_[1]
    n = (array[(i-1)% 10, (j-1)%10], array[(i-1)%10, j], array[(i-1)%10,(j+1)%10], array[i, (j-1)%10], array[i, (j+1)%10], 
        array[(i+1)%10, (j-1)%10], array[(i+1)%10, j], array[(i+1)%10, (j+1)%10])
    return int(sum(n))


#####
## **Rules of the game**
## If a living cell has 2 or 3 living neighbors, it stays alive
## If a dead cell has exactly 3 living neighbor, it comes alive
#####

# keys of the dictionary

# the dictionary will have the index of the cells as the keys and the value will be a list of two elements
# the first element will indicate whether the cell is dead or alive, and the second wil lhave the number of neighbors that are alive

def create_dic(array, shape):
    """shape is the dimension of the array, takes in an integer. Assumption of square array
    Creates a dictionary which has information of the starting array"""
    keys = []
    for i in range(shape):
        for j in range(shape):
            key = (i,j)
            keys.append(key)

    dic = dict.fromkeys(keys, [0,0])    # dictionary with [0, 0]

    # updating the values of the keys
    for k in dic:
        dic[k] = [array_(arr, k), neighbours_(arr, k)]

    return dic


### the rules of the game

def check_next_state(index, dic_):
    """takes in index of the cell and returns boolean on whether the cell state needs to change or not
    by checking the number of neighbors from the value in the dictionary"""
    # checking on dead cells
    if dic_[index][0] == 0:
        if dic_[index][1] == 3:
            return True
        else:
            return False
    else: # for cells that are alive
        if (dic_[index][1] == 2) or (dic_[index][1] == 3):
            return False
        else: 
            return True


def update_dic_state(dic_, array):
    """
    NEED TO CHANGE THIS:
    takes in dictionary containing state of current state,
    returns a tuple: (dictionary with updated state, set of cells that need to be updated for their neighbors)"""
    new_dic = dic_.copy()

    change_ = []      # list of indices which changes; dead -> alive, alive -> dead
    for k in dic_:
        if check_next_state(k, dic_):
            change_.append(k)
            if dic_[k][0] == 0:
                new_dic[k][0] == 1
            else:
                new_dic[k][0] == 0
    updated_array = update_array(array, change_)
    target_cells = get_target_cells(change_)
    #print(new_dic)
    #print("-----------------------------------")
    new_dic = update_dic_neighbor(new_dic, target_cells, updated_array)
    return new_dic,  updated_array


def get_target_cells(change_list):
    """takes in the change_ list created by update_dic_state and 
    returns a set containing all the cells that needs to be checked for next generation.
    That is, it appends the neighbors of the cells that would change whose neighbors will be calculated for the next generation"""
    target_cells = []
    n=10
    for cell in change_list:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                tup = ((cell[0] + i)%n, (cell[1] + j)%n)
                target_cells.append(tup)

    return set(target_cells)


def update_dic_neighbor(dic_, target_cells_, array):
    """takes in the result from the function update_dic_state and updated_array and 
    return updated dictionary for next generation"""
    new_dic = dic_.copy()

    for i in target_cells_:
        new_dic[i] = [dic_[i][0], neighbours_(array, i)]

    return new_dic


def update_array(array, change_):
    """will update the array by changing the indices from the change_ list"""
    newState = array.copy()    # creating a copy of the array
    # looping over the change_ list
    for i in change_:
        change_state(newState, i)

    return newState


def change_state(array, index):
    """changes state of the cell in the array"""
    if array_(array, index) == 0:
        array[index[0]][index[1]] = 1
    else:
        array[index[0]][index[1]] = 0

    




#==============================================================================
dic = create_dic(arr, 10)
stuff = update_dic_state(dic, arr)
new_dict, new_array = stuff[0], stuff[1]
#print(update_dic_state(dic, arr))
#for i in range(10):
#    #print(arr)
#    #print(dic)
#    stuff = update_dic_state(dic, arr)
#    dic = stuff[0]
#    
#    arr = stuff[1]



def start_game(grid, dic):
    """starts the game"""
    global SCREEN, CLOCK

    pygame.init()
    pygame.display.set_caption("Conways game of life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    import time
    dic_ = dic
    grid_ = grid
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        time.sleep(0.1)

        stuff = update_dic_state(dic_, grid_)
        dic_ = stuff[0]
        grid_ = stuff[1]
        block_size = 60

        for i, j in np.ndindex(9, 9):
            col = BLUE if grid_[i, j] == 1 else WHITE
            rect = pygame.Rect(j*block_size, i*block_size, block_size-1, block_size-1)
            pygame.draw.rect(SCREEN, col, rect)
    
        pygame.display.update()

def main():
    start_game(arr, dic)

#if __name__ == "__main__":
#    main()
#print(change((0,0)))
#print(dic)
#print(neighbours_(arr,1,0))
#print(arr)
#print(newState)
#print(change_)

#print(change((0,1)))
