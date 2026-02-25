# ingreDistr.py
import pygame
import os
import random
from vector import vec, pyVec
from constants import *
from drawable import Drawable
from gameEngine import GameEngine

PATH = "game sprites"

class IngredientDistribution(object):

    def __init__(self, imageCard):

        self.imageCard = imageCard

        self.allMeals = ["burger", "hotdog", "ramen"]
        self.mealPath = ""

        for meal in self.allMeals:
            if meal in self.imageCard:
                self.mealPath = f"{PATH}/{meal}"
                break

        self.ingredients = []
        self.engine = None

        self.load_ingredients()
        self.engine = GameEngine(self.ingredients)

   
    def load_ingredients(self):

        if not os.path.isdir(self.mealPath):
            print("Meal path does not exist:", self.mealPath)
            return

        for filename in os.listdir(self.mealPath):

            full_path = os.path.join(self.mealPath, filename)
            image = pygame.image.load(full_path).convert_alpha()

            MAX_SIZE = 50
            w, h = image.get_size()
            scale = min(MAX_SIZE / w, MAX_SIZE / h, 1)
            image = pygame.transform.smoothscale(
                image, (int(w * scale), int(h * scale))
            )

            x = random.randint(0, WORLD_SIZE[0] - image.get_width())
            y = random.randint(0, WORLD_SIZE[1] - image.get_height())

            self.ingredients.append((image, vec(x, y)))

    
    def handleEvent(self, event):
        self.engine.handleEvent(event)

   
    def update(self, seconds):
        self.engine.update(seconds)

   
    def draw(self, surface):

        surface.fill((255, 255, 255))

        for image, pos in self.ingredients:
            surface.blit(image, pyVec(pos - Drawable.CAMERA_OFFSET))

        self.engine.draw(surface)