import pygame
from drawable import Drawable
from vector import vec, pyVec
from constants import *

class World(object):

    def __init__(self):
        self.background = Drawable((0,0), "kitchen_floor.png")
        self.background.image = pygame.transform.scale(
            self.background.image,
            pyVec(WORLD_SIZE)
        )
    
    def handleEvent(self, event):
        pass

    def update(self, seconds):
        pass

    def draw(self, surface):

        surface.blit(
            self.background.image,
            pyVec(vec(0,0) - Drawable.CAMERA_OFFSET)
        )