'''Testing file for optimizing_1.py'''

from pygame.display import update
from optimizing_1 import *

## Testing for starting position to be glider

arr = starting_array((10,10))
add_Glider(0,0,arr)
print(arr)
# array_ takes coordinate as a tuple anr returns value 0 or 1
assert array_(arr,(2,3)) == arr[2][3] == 0
assert array_(arr, (0,0)) == arr[0][0] == 0

assert neighbours_(arr, (0,0)) == 1
assert neighbours_(arr, (0,1)) == 3

dic = create_dic(arr, 10)
print(dic)
assert dic[(0,0)] == [0,1]
assert dic[(0,1)] == [0,3]
assert dic[(1,2)] == [1,3]

assert check_next_state((0,0), dic) == False
assert check_next_state((0,1), dic) == True
assert check_next_state((1,2), dic) == False

assert array_(update_dic_state(dic, arr)[1], (0,1)) == 1
assert array_(update_dic_state(dic, arr)[1], (1,1)) == 0
assert array_(update_dic_state(dic, arr)[1], (1,0)) == 0

assert update_dic_state(dic, arr)[0][(0,1)][0] == 1
assert update_dic_state(dic, arr)[0][(1,1)][0] == 0
assert update_dic_state(dic, arr)[0][(1,0)][0] == 0