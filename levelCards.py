import pygame 
from card import Card

class LevelCards(object):
    def __init__(self):
        self.levelCards = {
            1: [Card("burgerCard.png", 2100), Card("hotdogCard.png", 2000), Card("ramenCard.png", 2300)],
            2: [Card("pizzaCard.png", 2700), Card("tacoCard.png", 3000), Card("sushiCard.png", 2900)],
            3: [Card("croissantCard.png", 3500), Card("friedRiceCard.png", 4000), Card("pastaCard.png", 3700)],
        }
    
    def get_level_cards(self, level):
        return self.levelCards[level]