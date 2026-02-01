import pygame 
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join

class SelectionScreen(object):
    def __init__(self):
        self.background = Drawable((0,0), "Selection Screen background.webp")
        self.background.image = pygame.transform.scale( self.background.image, (500, 350))
    
    def draw(self, surface):
        
        surface.fill((0,0,0))
        
        self.background.draw(surface)


    
    def handleEvent(self, event):
        
        pass