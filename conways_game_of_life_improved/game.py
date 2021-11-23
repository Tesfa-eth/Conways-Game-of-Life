"""
Play the game according to the rules
Display it in an interactive window using pygame

"""

from os import name
from time import sleep
from numpy.core.defchararray import array
import pygame
import pygame_menu
import numpy as np

from create_grids import pad_array, starting_array, add_Glider, add_Blinker, add_beacon, random_array

from button import Button 

BLUE = (34, 36, 128)
WHITE = (255,255,255)
BLACK = (0,0,0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
col = WHITE
grid_size = []

def get_neighbours(array, i, j):
    """returns all the 8 neighbours of a cell"""
    row, column = array.shape[0], array.shape[1]
    if i >= row-2 or j >= column-2:
        return (0,0,0,0,0,0,0,0)
    else:
        return (array[i-1, j-1], array[i-1, j], array[i-1,j+1], array[i, j-1], array[i, j+1], 
            array[i+1, j-1], array[i+1, j], array[i+1, j+1])


def remove_edges(neighbours):
    """takes in a tuple and removes the egdes from them"""
    neighbours_list = list(neighbours)
    #egdeless_neighbours = [ 0 if is_padding(x, padding) else int(x) for x in neighbours_list]
    return tuple(neighbours_list)

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
    #actual_neighbours = remove_edges(neighbours)
    neighbour_value = sum(list(neighbours))

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

def update_grid(array, block_size_y,block_size_x, start_update):
    """updates the grid and returns the new state"""
    btn_space = WINDOW_HEIGHT//20
    newState = np.zeros((array.shape[0], array.shape[1]))

    row, column = array.shape[0], array.shape[1]
    for i, j in np.ndindex(row, column):
        if start_update:
            #print("UPDATING") # debugging
            newState[i,j] = check_rule(array, i, j)
            col = BLACK if newState[i, j] == 1 else WHITE
            rect = pygame.Rect(j*block_size_y, i*block_size_x-btn_space, block_size_y-1, block_size_x-1)
            pygame.draw.rect(SCREEN, col, rect)
        else:
            #print("No UPDATE") # debugging
            newState = array
            col = BLACK if newState[i, j] == 1 else WHITE
            rect = pygame.Rect(j*block_size_y, i*block_size_x, block_size_y-1, block_size_x-1)
            pygame.draw.rect(SCREEN, col, rect)

    return newState

def customize(mouse_position, grid):
    block_size_height = WINDOW_HEIGHT//grid.shape[0]
    block_size_weight = WINDOW_WIDTH//grid.shape[1]
    i = mouse_position[0]//block_size_height
    j = mouse_position[1]//block_size_weight

    #print('shape', grid.shape) # debugging
    
    if i < grid.shape[0] and j < grid.shape[0]:
        grid[j][i] = 1
    return grid

def set_difficulty(value, difficulty):
    """select difficulty based on the value of the selector input"""
    difficulty_level = {0:10, 1:20, 2:35, 3:50, 4:75, 5:100, 6:120}
    grid_size.append(difficulty_level[value[1]])

def start_game():
    """starts the game"""
    global SCREEN, CLOCK
    no_of_btns = 5
    btn_height = WINDOW_HEIGHT//20 # leave a space to draw buttons
    btn_location_h = WINDOW_HEIGHT - btn_height # btn location from buttom screen
    btn_width = WINDOW_WIDTH//no_of_btns # button width for each button
    btn_location_w = WINDOW_WIDTH - btn_width # btn location from buttom screen

    pygame.init()
    pygame.display.set_caption("Conways game of life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    
    
    #Termination Button 
    pause_button = Button((255, 117, 117), WHITE, 0, btn_location_w-(btn_width*3), btn_location_h, btn_width, btn_height, 'Pause') #create quit button
    #stop_button.draw_rect(SCREEN) 
    
    #Pause Button 
    resume_button = Button((255, 173, 173),WHITE, 0, btn_location_w-(btn_width*2), btn_location_h, btn_width, btn_height, 'Resume')
    
    #Restart Button
    # color, x, y, width, height
    restart_button = Button((255, 117, 117),WHITE, 0, btn_location_w-(btn_width*1), btn_location_h, btn_width, btn_height, 'Restart')

    #Quit
    quit_button = Button((255, 87, 87),WHITE, 0, btn_location_w-(btn_width*0), btn_location_h, btn_width, btn_height, 'Quit')

    #Start    btn_location_w-(btn_width*4) gives us the exact location of the buttons
    start_button = Button((255, 87, 87), WHITE, 0, btn_location_w-(btn_width*4), btn_location_h, btn_width, btn_height, 'Start')
    
    #Menu
    menu_fonts = pygame_menu.font.FONT_NEVIS
    menu_theme = pygame_menu.Theme(background_color = BLACK,
                     title_background_color=BLACK, title_font_color= WHITE,
                     title_offset=(160,120), title_font_size = 48,
                     widget_padding= 5, widget_font=menu_fonts, 
                     widget_font_size = 20, widget_background_color = BLACK,
                     widget_border_color = BLACK, widget_border_width =0,
                     title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE)
    
    menu = pygame_menu.Menu('Game of Life', 600, 600, center_content = True, 
                            enabled = True, mouse_enabled = True, 
                            mouse_visible = True, 
                            theme = menu_theme)
    
    #Grid choice for selector
    choices = [('10 x 10', WHITE),('20 x 20', WHITE), ('35 x 35', WHITE), ('50 x 50', WHITE),('75 x 75', WHITE), 
    ('100 x 100', WHITE), ('120 x 120', WHITE)]
    choice = menu.add.selector(title='Choose grid:', items=choices,
                               style=pygame_menu.widgets.SELECTOR_STYLE_FANCY, onchange=set_difficulty)
        
    #Random start
    random_button = Button(WHITE, BLACK, 20,WINDOW_WIDTH//2-145, 
                           WINDOW_HEIGHT//2+140, WINDOW_WIDTH//3+90, 35, 
                           'Random Start')
    
    #Glider
    customize_button = Button(WHITE, BLACK, 20,WINDOW_WIDTH//8+80, 
                              WINDOW_HEIGHT//2+80, WINDOW_WIDTH//4+140, 35, 
                              'Customize')
    
    pause = False
    start = False
    update = False
    custom = False
    zoom_out = False
    zoom_in = False
    drag = False
    maximize = 0

    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    # create rectangle
    input_rect = pygame.Rect(WINDOW_WIDTH//3+100, WINDOW_HEIGHT//3+70, 5, 32)
    
    # color_active stores color(red) which
    # gets active when input box is clicked by user
    color_active = pygame.Color(194, 60, 60)
    color_passive = (196, 196, 196)
    color = color_passive
    active = False
    while True:
        if custom and drag: # clicked user input for mouse drag
            grid = customize(mouse_position, grid)
            
        events = pygame.event.get()
        for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # give option of drag or click for customization
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                    if resume_button.mouse_over(mouse_position):
                        pause = False
                    if pause_button.mouse_over(mouse_position):
                        pause = True
                    if restart_button.mouse_over(mouse_position):
                        main()

                    if start_button.mouse_over(mouse_position):
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

                        grid = random_array(start_x, start_y)
                        start = True
                    
                    if custom: # clicked user input for mouse click only
                        grid = customize(mouse_position, grid)

                    if customize_button.mouse_over(mouse_position):
                        try:
                            start_x = start_y = int(user_text) # take the starting gride size
                        except ValueError:
                            if grid_size:
                                start_x = start_y = grid_size[-1]
                            else:
                                start_x = start_y = 40
                        grid = starting_array((start_x,start_y))
                        custom = True
                        start = True
                        
                    if quit_button.mouse_over(mouse_position):
                        pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_o]: # zoom out
                        zoom_out = True
                    if pressed[pygame.K_i]: # zoom in
                        zoom_in = True
                    if pressed[pygame.K_d]: # enable custom dragging
                        drag = True
                    if pressed[pygame.K_s]: # stop custom dragging
                        drag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # when back space is hit
                        user_text = user_text[:-1]
                    else: # additional string
                        user_text += event.unicode


                   
        # get mouse position              
        mouse_position = pygame.mouse.get_pos()
        if start:
            SCREEN.fill(BLACK)
            if zoom_out and update:
                grid = pad_array(grid, 0)
                # print("maximizing now")
                maximize += 1
                zoom_out = False
            elif zoom_in and update:
                x = grid.shape[0]
                y = grid.shape[1]
                grid = grid[1:x-1, 1:y-1]
                zoom_in = False
            grid = update_grid(grid, WINDOW_WIDTH/grid.shape[1], WINDOW_HEIGHT/grid.shape[0], update)
            resume_button.draw_rect(SCREEN)
            pause_button.draw_rect(SCREEN)
            restart_button.draw_rect(SCREEN)
            quit_button.draw_rect(SCREEN)
            start_button.draw_rect(SCREEN)
        
        # before the game starts
        else:    
            #menu
            menu.update(events) 
            menu.draw(SCREEN)
            #subtitle
            myfont2 = pygame.font.SysFont('Nevis', 28)
            subtitle = myfont2.render('By Tesfa, Swagata, and Niki', False, WHITE)
            SCREEN.blit(subtitle,(165,205))
            version = myfont2.render('Version 1', False, WHITE)
            SCREEN.blit(version,(245,235))
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
    """main function"""
    start_game()


if __name__ == "__main__":
    main()