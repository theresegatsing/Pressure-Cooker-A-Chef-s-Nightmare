import pygame
from drawable import Drawable


CARD_WIDTH = 150
CARD_HEIGHT = 200
CARD_GAP = 20
TEXT_PADDING = 5

class Card(object):

    def __init__(self, image_path, description, points):
        self.drawable = Drawable((0, 0), image_path)
        self.drawable.image = pygame.transform.smoothscale(
            self.drawable.image, (CARD_WIDTH, CARD_HEIGHT)
        )
        self.description = description
        self.points = points
    
