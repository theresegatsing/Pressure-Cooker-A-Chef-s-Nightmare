import pygame 
from vector import *
import os
import random
RESOLUTION = vec(500,350)
SCALE =2
UPSCALED = RESOLUTION * SCALE

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
            image = pygame.transform.smoothscale(image, (int(w * scale), int(h * scale)))
            

            x = random.randint(0, max(0, RESOLUTION[0] - image.get_width()))
            y = random.randint(0, max(0, RESOLUTION[1] - image.get_height()))

            self.ingredients.append((image, vec(x, y)))

    

    def run(self):
        if self.mealPath == "":
            print("No valid meal found in image card.")
            return
        pygame.init()
        screen = pygame.display.set_mode(pyVec(UPSCALED))
        drawSurface = pygame.Surface(pyVec(RESOLUTION))

        self.load_ingredients()
        start_time = pygame.time.get_ticks()

        Running = True
        while Running:
            pygame.transform.scale(drawSurface, pyVec(UPSCALED), screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Running = False
            
            drawSurface.fill((255, 255, 255))

            for image, pos in self.ingredients:
                drawSurface.blit(image, pyVec(pos))

            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 #in seconds
            if elapsed_time > 30:
                Running = False
            
