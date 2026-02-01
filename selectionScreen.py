import pygame 
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from PIL import Image

class SelectionScreen(object):
    def __init__(self):
        
        self.background = Drawable((0,0), "Selection Screen background.jpg")
        self.background.image = pygame.transform.smoothscale( self.background.image, (500, 350))
        self.burgerCard = Drawable((40,60),  "burger card.png")
        self.burgerCard.image = pygame.transform.smoothscale(self.burgerCard.image, (150, 200))
    
    def draw(self, surface):
        
        surface.fill((0,0,0))
        
        self.background.draw(surface)
        self.burgerCard.draw(surface)


    
    def handleEvent(self, event):
        
        pass