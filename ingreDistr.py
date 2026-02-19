import pygame 
from gameEngine import Drawable, GameEngine
from vector import *
import os
import random
from constants import *

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
        self.start_time = 0

    def start(self):
        if self.mealPath == "":
            print("No valid meal found in image card.")
            return

        self.load_ingredients()
        self.engine = GameEngine(self.ingredients)
        self.start_time = pygame.time.get_ticks()

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
                image,
                (int(w * scale), int(h * scale))
            )

            x = random.randint(0, max(0, WORLD_SIZE[0] - image.get_width()))
            y = random.randint(0, max(0, WORLD_SIZE[1] - image.get_height()))

            self.ingredients.append((image, vec(x, y)))

    def handleEvent(self, event):
        if self.engine:
            self.engine.handleEvent(event)

    def update(self, seconds):
        if self.engine:
            self.engine.update(seconds)

        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed_time > 120:
            Drawable.CAMERA_OFFSET = vec(0, 0)

    def draw(self, surface):
        surface.fill((255, 255, 255))

        for image, pos in self.ingredients:
            surface.blit(image, pyVec(pos - Drawable.CAMERA_OFFSET))

        if self.engine:
            self.engine.draw(surface)