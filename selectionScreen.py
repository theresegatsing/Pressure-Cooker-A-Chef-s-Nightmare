import pygame 
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from PIL import Image
from card import Card 
import random 
from vector import vec
from game import Game
from ingreDistr import IngredientDistribution
from constants import *
from levelCards import LevelCards

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 350
SCALE = 2

CARD_WIDTH = 110
CARD_HEIGHT = 160
SIDE_MARGIN = 30
TEXT_PADDING = 5




class SelectionScreen(object):
    def __init__(self, level):
        
        self.background = Drawable((0,0), "Selection Screen background.jpg")
        self.background.image = pygame.transform.smoothscale( self.background.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        
        self.allCards = LevelCards().get_level_cards(level)

        #self.selectedCards = random.sample(self.allCards, 3)
        self.selectedCards = self.allCards
        self.position_cards_centered()

    
    def position_cards_centered(self):
        available_width = SCREEN_WIDTH - 2 * SIDE_MARGIN
        num_cards = len(self.selectedCards)

        if num_cards > 1:
            card_gap = (available_width - num_cards * CARD_WIDTH) // (num_cards - 1)
        else:
            card_gap = 20

        start_x = SIDE_MARGIN
        y = 80

        for i, card in enumerate(self.selectedCards):
            x = start_x + i * (CARD_WIDTH + card_gap)
            card.drawable.position = vec(x, y)


    def draw(self, surface):
        self.background.draw(surface)

        for card in self.selectedCards:
            card.drawable.draw(surface)

    

    def handleEvent(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = vec(*event.pos) // SCALE

            for card in self.selectedCards:
                if card.drawable.getCollisionRect().collidepoint(mouse_pos):
                    return (card.image_path, card.points)
        
       