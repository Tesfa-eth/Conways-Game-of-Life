"""
Testing the functions inside the creat_grids.py and game.py
"""

import numpy as np
from numpy import testing
from game import get_neighbours, is_alive, is_padding, remove_edges
from create_grids import pad_array


def run_tests():
    test_array = np.array([[1,2,3], [4,5,6]])
    expected_array = np.array([[9,9,9,9,9],[9,1,2,3,9], [9,4,5,6,9], [9,9,9,9,9]])
    assert pad_array(test_array, 9).all() == np.array([[9,9,9,9,9],[9,1,2,3,9], [9,4,5,6,9], [9,9,9,9,9]]).all()
    testing.assert_array_equal(pad_array(test_array, 9), expected_array, err_msg='', verbose=True)
    assert get_neighbours(expected_array, 2,2) == (1,2,3,4,6,9,9,9)
    assert is_padding(9,9) == True
    assert remove_edges((1,1,9,0,0,9,9,9), padding=9) == (1,1,0,0,0,0,0,0)
    assert is_alive(1) == True
    assert is_alive(0) == False


if __name__ == "__main__":
    run_tests()
