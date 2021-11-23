"""
Conway's Game of Life Simulation
-----------------------------------
create_grids.py
-----------------------------------
This utility file: creates grids, offers different 
sample starting points, padding.
Functions: starting_array(shape=window_size), pad_array(array, _with=padding), add_Glider(i, j, array), add_Blinker(i, j, array), add_beacon(i, j, array), random_array(x, y). 
Note: Used in game.py
------------------------------------
Bennington College - Tesfa, Swag, Niki - Coding Workshop 2021
"""

import numpy as np

padding = 6
window_size = (10, 10)


def starting_array(shape=window_size):
    """gives us a window (array) of specific shape"""
    return np.zeros((shape))


def pad_array(array, _with=padding):
    """pads the array/window with specific constant _with"""
    return np.pad(array, 1, mode='constant', constant_values=(_with))


def add_Glider(i, j, array):
    """glider starting point"""
    glider = np.array([[0, 0, 1],
                       [1, 0, 1],
                       [0, 1, 1]])
    array[i:i+3, j:j+3] = glider


def add_Blinker(i, j, array):
    """blinker starting point"""
    blinker = np.array([[0, 1, 0],
                       [0, 1, 0],
                       [0, 1, 0]])
    array[i:i+3, j:j+3] = blinker


def add_beacon(i, j, array):
    """beacon starting position"""
    beacon = np.array([[1, 1, 0, 0],
                       [1, 1, 0, 0],
                       [0, 0, 1, 1],
                       [0, 0, 1, 1]])
    array[i:i+4, j:j+4] = beacon


def random_array(x, y):
    """generates a random array of x, y dimensions"""
    return np.random.randint(0, 2, (x, y)) 