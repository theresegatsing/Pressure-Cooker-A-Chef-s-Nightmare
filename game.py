import pygame 
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
from selectionScreen import *


class Game(object):

    def __init__(self, image_path, points):
        self.image_path = image_path
        self.points = points
        self.state = IngredientDistribution(image_path)

        self.timeLimit = 90.0
        self.elapsed = 0.0
        self.finished = False

    def handleEvent(self, event):
        self.state.handleEvent(event)

    def update(self, seconds):
        if self.finished:
            return

        self.elapsed += seconds

        if self.elapsed >= self.timeLimit:
            self.finished = True
            return

        self.state.update(seconds)

    def draw(self, surface):
        self.state.draw(surface)