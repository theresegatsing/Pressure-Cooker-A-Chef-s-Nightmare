import pygame 
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
from selectionScreen import *


class Game(object):

    def __init__(self, image_path, points):
        self.image_path = image_path
        self.points = points
        self.state = IngredientDistribution(image_path)

    def handleEvent(self, event):
        self.state.handleEvent(event)

    def update(self, seconds):
        self.state.update(seconds)

    def draw(self, surface):
        self.state.draw(surface)