# world.py
import pygame
from drawable import Drawable
from vector import vec, pyVec
from constants import *

class World(object):

    def __init__(self):

        self.tree = Drawable((0,0), "t2.png")
        self.tree.image = pygame.transform.scale(
            self.tree.image,
            pyVec(WORLD_SIZE)
        )

    def handleEvent(self, event):
        pass

    def update(self, seconds):
        pass
 
    def draw(self, surface):
        surface.fill((255,0,0))

     #  self.tree.draw(surface)