import pygame 
from card import Card

class LevelCards(object):

    def __init__(self, level):

        self.level = level

        self.levelCards = {2: [Card("burgerCard.png", 
                2100)
        ]}
    
    def get_cards(self):
        return self.levelCards[self.level]