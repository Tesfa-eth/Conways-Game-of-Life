import matplotlib
#from matplotlib import pyplot
import matplotlib.pyplot as plt
#from matplotlib.pyplot import xlabel, ylabel
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *

import pylab

def draw_graph(list_):
    fig = plt.figure(figsize=[4, 4], # Inches
                    dpi=150      # 100 dots per inch, so the resulting buffer is 400x400 pixels
                    )
    
    
    ax = fig.gca()
    plt.xlabel('Generation')
    plt.ylabel('Number of alive cells')
    ax.plot(list_)
    

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    pygame.init()

    window = pygame.display.set_mode((600, 600), DOUBLEBUF)
    screen = pygame.display.get_surface()

    size = canvas.get_width_height()

    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0,0))
    pygame.display.flip()

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True


#draw_graph([1, 2, 4,6,8,9,10,25,35])