import pygame 
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
from selectionScreen import *


class Game(object):

    def __init__(self, image_path, points):
        self.image_path = image_path
        self.points = points

    def run(self):
        
        IngredientDistribution(self.image_path).run()
        