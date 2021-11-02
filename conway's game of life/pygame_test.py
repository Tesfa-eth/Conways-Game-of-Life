# Python code to implement Conway's Game Of Life
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import testing
from numpy.core.fromnumeric import shape

padding = 6
window_size = (5,5)
def add_Glider(i,j, array):
    # extracted from GeeksforGeeks
    glider = np.array([[0, 0, 1],
                       [1, 0, 1],
                       [0, 1, 1]])
    array[i:i+3, j:j+3] = glider

def add_Blinker(i,j,array):
    blinker = np.array([[0, 1, 0],
                       [0, 1, 0],
                       [0, 1, 0]])
    array[i:i+3, j:j+3] = blinker
def starting_array(shape=window_size):
    """gives us a window (array) of specific shape"""
    return np.zeros((shape))

def pad_array(array, _with):
    """pads the array/window with specific constant _with"""
    return np.pad(array, 1, mode='constant', constant_values = (_with))

def is_padding(cell, padding):
    return cell == padding

def get_neighbours(array, i, j):
    """returns all the 8 neighbours of a cell"""
    return (array[i-1, j-1], array[i-1, j], array[i-1,j+1], array[i, j-1], array[i, j+1], 
        array[i+1, j-1], array[i+1, j], array[i+1, j+1])

def remove_edges(neighbours, padding=padding):
    """takes in a tuple and removes the egdes from them"""
    neighbours_list = list(neighbours)
    egdeless_neighbours = [ 0 if is_padding(x, padding) else int(x) for x in neighbours_list]
    return tuple(egdeless_neighbours)

def is_alive(cell):
    return True if cell == 1 else False

def check_rule(array,i, j):
    """
    cell - the cell it self
    i,j - the location of the cell in the grid
    return: bool
    """
    neighbours = get_neighbours(array, i, j)
    actual_neighbours = remove_edges(neighbours)
    neighbour_value = sum(list(actual_neighbours))

    if is_alive(array[i,j]):
        print(array[i,j], neighbours)
        if neighbour_value == 2 or neighbour_value == 3:
            return 1
        else:
            return 0

    else:
        if neighbour_value == 3:
            return 1
        else:
            return 0

def update_array(array):
    row, column = shape(array)[0], shape(array)[1]
    for i in range(row-1):
        for j in range(column-1):
            if not is_padding(array[i,j], padding=69):
                array[i,j] = check_rule(array, i, j)

    return array

array = starting_array((7,7))
padded_array = pad_array(array, 69)
add_Blinker(2,2, padded_array)
print(padded_array)
#print(update_array(padded_array))
#print(get_neighbours(padded_array,3,3))