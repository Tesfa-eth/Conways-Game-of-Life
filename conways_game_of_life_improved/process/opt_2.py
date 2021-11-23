'''
Adding buttons and other stuff. Updating on  optimizing_1.py

Compatible with rectangular array
'''
from os import name
from numpy.core.defchararray import array
import pygame
import numpy as np
import random 

from create_grids import add_random, random_array, add_Glider,  starting_array, add_beacon, add_Blinker

BLUE = (34, 36, 128)
WHITE = (200,200,200)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
RED = (255, 0, 0)
col = WHITE

#n2 = 60 
#n1 = 30


def create_array(x, y):
    global n1 
    global n2 
    n1 = x
    n2 = y
    arr = starting_array((n1, n2))
    return arr

def add_to_array(array, type_, x, y, size = 0):
    """array: to the array that stuff would be added
    type: add_random, add_Glider, add_beacon, add_Blinker
    x, y : position where the stuff is to be added
    size: only required for add_random, in which case its the size of the array. Assumed to be square """
    if type_ == add_random:
        add_random(size, array, x, y)
    elif type_ == add_Glider:
        add_Glider(x, y, array)
    elif type_ == add_beacon:
        add_beacon(x, y, array)
    elif type_ == add_Blinker:
        add_Blinker(x, y, array)
    


def array_(array, index_):
    """gives the value of the cell meaning 0 or 1. Takes in a tumple of (row, column)"""
    return array[index_[0], index_[1]]




def neighbours_(array, index_):
    """calculates the number of living neighbors"""
    i = index_[0]
    j = index_[1]
    num = (array[(i-1)% n1, (j-1)%n2], array[(i-1)%n1, j], array[(i-1)%n1,(j+1)%n2], array[i, (j-1)%n2], array[i, (j+1)%n2], 
        array[(i+1)%n1, (j-1)%n2], array[(i+1)%n1, j], array[(i+1)%n1, (j+1)%n2])
    return int(sum(num))


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
    for i in range(shape[0]):
        for j in range(shape[1]):
            key = (i,j)
            keys.append(key)

    dic = dict.fromkeys(keys, [0,0])    # dictionary with [0, 0]

    # updating the values of the keys
    for k in dic:
        dic[k] = [array_(array, k), neighbours_(array, k)]

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
                new_dic[k] = [1, dic_[k][1]]
            else:
                new_dic[k] = [0, dic_[k][1]]
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
    for cell in change_list:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                tup = ((cell[0] + i)%n1, (cell[1] + j)%n2)
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

        time.sleep(0.05)

        stuff = update_dic_state(dic_, grid_)
        dic_ = stuff[0]
        grid_ = stuff[1]
        block_size_r = WINDOW_HEIGHT//n1
        block_size_c = WINDOW_WIDTH//n2
        list_ = [BLACK, BLUE, RED, GREEN]
        for i, j in np.ndindex(n1, n2):
            #col = random.choice(list_)

            no1 = random.randint(0,255)
            no2 = random.randint(0,255)
            no3 = random.randint(0,255)
            col = (no1, no2, no3)

            col = col if grid_[i, j] == 1 else (50,50,50)
            rect = pygame.Rect(j*block_size_c, i*block_size_r, block_size_c-1, block_size_r-1)
            pygame.draw.rect(SCREEN, col, rect)
    
        pygame.display.update()

def main():
    arr = create_array(40, 40)
    add_to_array(arr, add_random, 5, 5, 20)
    print(n1, n2)
    start_game(arr, create_dic(arr,(n1, n2)))

if __name__ == "__main__":
    main()

