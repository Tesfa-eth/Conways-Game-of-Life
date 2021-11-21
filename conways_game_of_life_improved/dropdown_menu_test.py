import pygame_menu  
import pygame


pygame.init()
pygame.display.set_caption("Conways game of life")
SCREEN = pygame.display.set_mode((700,700))
CLOCK = pygame.time.Clock()
SCREEN.fill((0,0,0))

black = (0,0,0)
white = (255,255,255)


dropdown_menu = pygame_menu.Menu('Game of Life', 700, 700, center_content = True, enabled = True, mouse_enabled = True, mouse_visible = True, theme = pygame_menu.themes.THEME_DARK)

button1 = pygame_menu.widgets.Button('click me')

choices = [('2 x 2', white), ('5 x 5', white)]
choice = dropdown_menu.add.selector(title='Choose grid', items=choices, style=pygame_menu.widgets.SELECTOR_STYLE_FANCY)

while True:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        

    if dropdown_menu.is_enabled():
        dropdown_menu.update(events)
        dropdown_menu.draw(SCREEN)

    pygame.display.update()

