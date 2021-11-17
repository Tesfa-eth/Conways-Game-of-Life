'''
This creates the buttons and places them on the bottom of the GUI
'''
import pygame 

class Button():
    def __init__(self, color, x, y, width, height, text = ' '):
        self.color = color  
        self.x = x #int
        self.y = y #int
        self.width = width #int
        self.height = height #int
        self.text = text #string
        
    def draw_rect(self, surface):
        
        white_color = (255, 255, 255)
        #color_button = (170, 170, 170)
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0, 15)
        
        if self.text != ' ':
            letter_font = pygame.font.SysFont('Corbel', 33) #fonts for the button
            text = letter_font.render(self.text, True, white_color)
            surface.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    def mouse_over(self, mouse_position):
        #mouse_position = pygame.mouse.get()
        if mouse_position[0] > self.x and mouse_position[0] < self.x + self.width:
            if mouse_position[1] > self.y and mouse_position[1] < self.y + self. height:
                return True
        return False
    
    def pause_game():
        
        while event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
                
 
