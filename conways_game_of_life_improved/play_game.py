"""
Conway's Game of Life Simulation
-----------------------------------
play_game.py
-----------------------------------
Language: Python
GUI Package: Pygame
GUI Menu Package: Pygame_menu
------------------------------------
Type of game: zero-player
Rules:
1) Any live cell with two or three live neighbours survives.
2) Any dead cell with three live neighbours becomes a live cell.
3) All other live cells die in the next generation. Similarly, all other dead cells stay dead.
------------------------------------
How to play:
* Type Number: user can type an integer, which creates a grid based on the given number.
* Customize button: selects the starting position of the alive cells.
* Random Start button: selects a random position of the alive cells.
* Start button: starts the game.
* Pause button: pauses the game at the point it was stopped.
* Resume button: resumes the game from the point it was paused earlier. 
* Restart button: brings the user back to the menu page and restarts the game.
* Quit button: stops the game completely and closes the GUI window.
Note: used dictionary for the optimization. 
* Statistics button: shows a graph of the number of alive cells over 
Keys of the dictionary:
1) The dictionary will have the index of the cells as the keys and the value 
will be a list of two elements.
2) The first element will indicate whether the cell is dead or alive, and 
the second wil lhave the number of neighbors that are alive
------------------------------------
Bennington College - Tesfa, Swagata, Niki - Coding Workshop 2021
"""

from os import name
from numpy.core.defchararray import array
import pygame
import pygame_menu
import numpy as np
import random 

from create_grids import add_random, random_array, add_Glider,  starting_array, add_beacon, add_Blinker
from graph_drawing import *
from button import Button 


BLUE = (34, 36, 128)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
RED = (255, 0, 0)
col = WHITE
grid_size = [10]
start_x = 40
start_y = 40
def create_array(x, y):
    """returns an array"""
    global n1 
    global n2 
    n1 = x
    n2 = y
    arr = starting_array((n1, n2))
    return arr

def add_to_array(array, type_, x, y, size = 0):
    """array: to the array that stuff would be added
       type: add_random, add_Glider, add_beacon, add_Blinker
       x, y : coordinates for different positions to be added on the grid
       size: only required for add_random, in which case its the size of the array.              Assumed to be square 
     """
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
    num = [0 if i == 5 else i for i in num]
    return int(sum(num))

def create_dic(array, shape):
    """Creates a dictionary which has information of the starting array.
       Parameter: Shape is the dimension of the array, takes in an integer. 
       Assumption of the array.
    """
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

########### the rules of the game #############
def check_next_state(index, dic_):
    """takes in index of the cell and returns boolean on whether 
       the cell state needs to change or not by checking the number
       of neighbors from the value in the dictionary"""
    # checking on dead cells
    if dic_[index][0] == 0:
        if dic_[index][1] == 3:
            return True
        else:
            return False
    elif dic_[index][0] == 5:
        if dic_[index][1] == 3:
            return True
        else:
            return False            
    else: # for cells that are alive
        if (dic_[index][1] == 2) or (dic_[index][1] == 3):
            return False
        else: 
            return True

def update_dic_state(dic_, array, update_state):
    """
    NEED TO CHANGE THIS:
    takes in dictionary containing state of current state,
    returns a tuple: (dictionary with updated state, set of cells that need to be updated for their neighbors)"""
    new_dic = dic_.copy()

    if update_state:
        change_ = []      # list of indices which changes; dead -> alive, alive -> dead
        for k in dic_:
            if check_next_state(k, dic_):
                change_.append(k)
                if dic_[k][0] == 0:
                    new_dic[k] = [1, dic_[k][1]]
                elif dic_[k][0] == 5:
                    new_dic[k] = [1, dic_[k][1]]
                else:
                    new_dic[k] = [5, dic_[k][1]]
        updated_array = update_array(array, change_)
        target_cells = get_target_cells(change_)
        #print(new_dic)
        #print("-----------------------------------")
        new_dic = update_dic_neighbor(new_dic, target_cells, updated_array)
        
        return new_dic,  updated_array
    else:
        return new_dic, array

def get_target_cells(change_list):
    """takes in the change_ list created by update_dic_state and 
       returns a set containing all the cells that needs to be checked 
       for next generation. That is, it appends the neighbors of the 
       cells that would change whose neighbors will be calculated for 
       the next generation"""
    target_cells = []
    for cell in change_list:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                tup = ((cell[0] + i)%n1, (cell[1] + j)%n2)
                target_cells.append(tup)

    return set(target_cells)

def update_dic_neighbor(dic_, target_cells_, array):
    """takes in the result from the function update_dic_state and 
    updated_array and returns updated dictionary for next generation"""
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
    if array_(array, index) == 0 or array_(array, index) == 5:
        array[index[0]][index[1]] = 1
    else:
        array[index[0]][index[1]] = 5

##############################
# customizing grid
def customize(mouse_position, grid):
    """returns a new customized grid of alive cells"""
    block_size_height = WINDOW_HEIGHT//grid.shape[0]
    block_size_weight = WINDOW_WIDTH//grid.shape[1]
    i = mouse_position[0]//block_size_height
    j = mouse_position[1]//block_size_weight
    
    if i < grid.shape[0] and j < grid.shape[0]:
        grid[j][i] = 1
    return grid

def set_difficulty(value, difficulty):
    """select difficulty based on the value of the selector input"""
    difficulty_level = {0:10, 1:20, 2:50, 3:120}
    grid_size.append(difficulty_level[value[1]])

###################################

def start_game():
    """starts the game"""
    global SCREEN, CLOCK
    global start_x, start_y
    alive_list = []
    array_list = []

    no_of_btns = 6
    btn_height = WINDOW_HEIGHT//20 # leave a space to draw buttons
    btn_location_h = WINDOW_HEIGHT - btn_height # btn location from buttom screen
    btn_width = WINDOW_WIDTH//no_of_btns # button width for each button
    btn_location_w = WINDOW_WIDTH - btn_width # btn location from buttom screen


    gen = 0
    
    pygame.init()
    pygame.display.set_caption("Conways game of life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    #Pause Button 
    pause_button = Button((255, 117, 117), WHITE, 0, 
                          btn_location_w-(btn_width*3), btn_location_h, 
                          btn_width, btn_height, 'Pause')
    
    #Resume Button 
    resume_button = Button((255, 173, 173),WHITE, 0, 
                           btn_location_w-(btn_width*2), btn_location_h, 
                           btn_width, btn_height, 'Resume')
    #Restart Button
    # color, x, y, width, height
    restart_button = Button((255, 117, 117),WHITE, 0, 
                            btn_location_w-(btn_width*1), btn_location_h, 
                            btn_width, btn_height, 'Restart')
    #Quit Button
    quit_button = Button((255, 87, 87),WHITE, 0, btn_location_w-(btn_width*0),
                         btn_location_h, btn_width, btn_height, 'Quit')
    #Start Button
    start_button = Button((255, 87, 87), WHITE, 0, btn_location_w-(btn_width*4),
                          btn_location_h, btn_width, btn_height, 'Start')
    #Stat Button
    stat_button = Button((255, 87, 87), WHITE, 0, btn_location_w-(btn_width*5),
                          btn_location_h, btn_width, btn_height, 'Statistics')
    
    ######################## MENU ########################
    menu_fonts = pygame_menu.font.FONT_NEVIS
    #create theme
    menu_theme = pygame_menu.Theme(background_color = BLACK,
                     title_background_color=BLACK, title_font_color= WHITE,
                     title_offset=(160,130), title_font_size = 48,
                     widget_padding= 5, widget_font=menu_fonts, 
                     widget_font_size = 20, widget_background_color = BLACK,
                     widget_border_color = BLACK, widget_border_width =0,
                     title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE)
    
    menu = pygame_menu.Menu('Game of Life', 600, 600, center_content = True, 
                            enabled = True, mouse_enabled = True, 
                            mouse_visible = True, 
                            theme = menu_theme)
    
    #Slider Bar to choose the grid measurments 
    choices = [('10 x 10', WHITE), ('20 x 20', WHITE), ('50 x 50', WHITE), ('100 x 100', WHITE)]
    choice = menu.add.selector(title='Choose grid:', items=choices,
                               style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
                               onchange=set_difficulty)

    #Random start Button
    random_button = Button(WHITE, BLACK, 20,WINDOW_WIDTH//2-145, 
                           WINDOW_HEIGHT//2+140, WINDOW_WIDTH//3+90, 35, 
                           'Random Start')
    
    #Glider Button
    customize_button = Button(WHITE, BLACK, 20,WINDOW_WIDTH//8+80, 
                              WINDOW_HEIGHT//2+80, WINDOW_WIDTH//4+140, 35, 
                              'Customize')
    ###############################################
    
    import time
    pause = False
    start = False #changed from True to False
    update = False
    custom = False
    
    # color_active stores color(red) which
    # gets active when input box is clicked by user
    color_active = pygame.Color(194, 60, 60)
    color_passive = (196, 196, 196)
    color = color_passive
    active = False
    

    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    # create rectangle for the user input
    input_rect = pygame.Rect(WINDOW_WIDTH//3+100, WINDOW_HEIGHT//3+70, 5, 32)
    game = False
    while not game:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.mouse_over(mouse_position):
                    pause = False
                    update = True
                    
                if pause_button.mouse_over(mouse_position):
                    pause = True
                    update = False
                
                if restart_button.mouse_over(mouse_position):
                    grid_size.append(10)
                    main()

                if start_button.mouse_over(mouse_position):
                    #start update
                    update = True
                    custom = False
                    
                if random_button.mouse_over(mouse_position):
                    try:
                        start_x = start_y = int(user_text) # take the starting gride size
                    except ValueError:
                        if grid_size:
                            start_x = start_y = grid_size[-1]
                        else:
                            start_x = start_y = 40                
                    grid_ = create_array(start_x, start_y)
                    add_to_array(grid_, add_random, 0, 0, start_x//2)
                    dic_ = create_dic(grid_, (start_x, start_y))
                    start = True
                
                if customize_button.mouse_over(mouse_position):
                    try:
                        start_x = start_y = int(user_text) # take the starting gride size
                    except ValueError:
                        if grid_size:
                            start_x = start_y = grid_size[-1]
                        else:
                            start_x = start_y = 40
                    grid_ = create_array(start_x, start_y)
                    custom = True
                    start = True
                if custom: # clicked user input for mouse click only
                    grid_ = customize(mouse_position, grid_)
                    dic_ = create_dic(grid_, (start_x, start_y))    
                       

                if quit_button.mouse_over(mouse_position):
                    game = True

                # statistics
                if stat_button.mouse_over(mouse_position):
                    game = True
                    draw_graph(alive_list)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # when back space is hit
                    user_text = user_text[:-1]
                else: # additional string
                    user_text += event.unicode

                    
        mouse_position = pygame.mouse.get_pos() # tuple of x, y coordinates 

        
        if start:

            SCREEN.fill(BLACK)
            #####################
            if update:
                array_list.append(grid_)

            stuff = update_dic_state(dic_, grid_, update)
            alive = sum([1 for i in dic_ if dic_[i][0] == 1])
            alive_button = Button((245, 186, 184),BLACK, 20, 10, 10, 200, 50, 
                                  f'Alive:{alive}')
            if update:
                alive_list.append(alive)
                
            dic_ = stuff[0]
            grid_ = stuff[1]
            ####################
        
            #time.sleep(0.1)

            ###################
            if update:
                gen+=1
            gen_button = Button((196, 73, 69),BLACK, 20, 390, 10, 200, 50,
                                f'Generation:{gen}')
            block_size_r = WINDOW_HEIGHT//n1
            block_size_c = WINDOW_WIDTH//n2
            list_ = [BLACK, BLUE, RED, GREEN]
            for i, j in np.ndindex(n1, n2):
                if grid_[i,j] == 1:
                    col = BLUE
                if grid_[i,j] == 5:
                    col = (240,210,210,0.1)
                if grid_[i,j] == 0:
                    col = (50, 50, 50)
                rect = pygame.Rect(j*block_size_c, i*block_size_r, block_size_c-1, block_size_r-1)
                pygame.draw.rect(SCREEN, col, rect)
        
        
            resume_button.draw_rect(SCREEN)
            start_button.draw_rect(SCREEN)
            pause_button.draw_rect(SCREEN)
            restart_button.draw_rect(SCREEN)
            quit_button.draw_rect(SCREEN)
            gen_button.draw_rect(SCREEN)
            alive_button.draw_rect(SCREEN)
            stat_button.draw_rect(SCREEN)
        
   

        else:
            #menu
            menu.update(events) 
            menu.draw(SCREEN)
            
            #subtitle
            myfont2 = pygame.font.SysFont('Nevis', 28)
            myfont3 = pygame.font.SysFont('Nevis', 22)
            subtitle = myfont2.render('By Tesfa, Swagata, and Niki', False, WHITE)
            SCREEN.blit(subtitle,(165,220))
            version = myfont3.render('Version 2', False, WHITE)
            SCREEN.blit(version,(265,250))
            
            #message for user input
            myfont3 = pygame.font.SysFont('Nevis', 25)
            type_msg = myfont3.render('Type Number:', False, WHITE)
            SCREEN.blit(type_msg,(WINDOW_WIDTH//3-20, WINDOW_HEIGHT//3+77))
    
            random_button.draw_rect(SCREEN)
            customize_button.draw_rect(SCREEN)
            # text input
            if active:
                color = color_active
            else:
                color = color_passive
            
            pygame.draw.rect(SCREEN, color, input_rect, border_radius=20)
            text_surface = base_font.render(user_text, True, WHITE)
            SCREEN.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(100, text_surface.get_width()+10)
            pygame.display.flip()
        
        if pause == False:
            pygame.display.update()
        

def main():
    start_game()

if __name__ == "__main__":
    main()

