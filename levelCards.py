import pygame 
from card import Card

class LevelCards(object):
    def __init__(self):
        self.levelCards = {
            1: [Card("burgerCard.png", 2100), Card("hotdogCard.png", 2000), Card("ramenCard.png", 2300)],
            2: [Card("pizzaCard.png", 2700), Card("tacoCard.png", 3000)]
        }
    
    def get_level_cards(self, level):
        return self.levelCards[level]