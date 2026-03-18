# ingreDistr.py
from math import dist
from pydoc import text

import pygame
import os
import random
from vector import vec, pyVec
from constants import *
from drawable import Drawable
from gameEngine import GameEngine

PATH = "game sprites"

class IngredientDistribution(object):

    def __init__(self, imageCard, thresholdPoints):

        #Drawing the background

        self.tree = Drawable((0,0), "bwt.jpg")
        self.tree.image = pygame.transform.scale(
            self.tree.image,
            pyVec(WORLD_SIZE)
        )


        # Storing the image card for later use in determining which meal to load
        self.imageCard = imageCard
        self.thresholdPoints = thresholdPoints
        self.currentPoints = 0


        self.allMeals = ["burger", "hotdog", "ramen"]
        self.mealPath = ""

        for meal in self.allMeals:
            if meal in self.imageCard:
                self.mealPath = f"{PATH}/{meal}"
                break

        self.ingredients = []
        self.engine = None

        self.load_ingredients()
        self.pointsPerIngredient = thresholdPoints // len(self.ingredients)

        for ing in self.ingredients:
            ing["points"] = self.pointsPerIngredient

        self.engine = GameEngine(self.ingredients, self)

        self.font = pygame.font.SysFont(None, 18)


    def make_grey(self, image):
        grey = image.copy()
        arr = pygame.surfarray.pixels3d(grey)
        avg = arr.mean(axis=2, keepdims=True)
        arr[:] = avg
        del arr
        return grey

    def load_ingredients(self):

        if not os.path.isdir(self.mealPath):
            print("Meal path does not exist:", self.mealPath)
            return

        for filename in os.listdir(self.mealPath):

            full_path = os.path.join(self.mealPath, filename)
            image = pygame.image.load(full_path).convert_alpha()

            # Remove near-white background pixels
            arr_rgb = pygame.surfarray.pixels3d(image)
            arr_alpha = pygame.surfarray.pixels_alpha(image)

            # Detect near-white pixels
            white = (
                (arr_rgb[:, :, 0] > 240) &
                (arr_rgb[:, :, 1] > 240) &
                (arr_rgb[:, :, 2] > 240)
            )

            arr_alpha[white] = 0

            del arr_rgb
            del arr_alpha

            # Scale down the image if it's too large

            MAX_SIZE = 50
            w, h = image.get_size()
            scale = min(MAX_SIZE / w, MAX_SIZE / h, 1)
            image = pygame.transform.smoothscale(
                image, (int(w * scale), int(h * scale))
            )

            image.set_colorkey((255,255,255), pygame.RLEACCEL)

            x = random.randint(0, WORLD_SIZE[0] - image.get_width())
            y = random.randint(0, WORLD_SIZE[1] - image.get_height())

            grey = self.make_grey(image)

            self.ingredients.append({
                "image": image,
                "grey": grey,
                "pos": vec(x, y),
                "collected": False,
                "upgrade_level" : 0,
                "points": 0
            })

    
    def handleEvent(self, event):
        self.engine.handleEvent(event)

   
    def update(self, seconds):
        self.engine.update(seconds)


    def draw(self, surface):

        self.tree.draw(surface)

        for ing in self.ingredients:
            if not ing["collected"]:
                surface.blit(
                    ing["image"],
                    pyVec(ing["pos"] - Drawable.CAMERA_OFFSET)
                )

        icon_size = 30
        padding = 10
        x_offset = RESOLUTION[0] - padding

        for ing in reversed(self.ingredients):

            icon = ing["image"] if ing["collected"] else ing["grey"]
            small_icon = pygame.transform.smoothscale(icon, (icon_size, icon_size))

            x_offset -= icon_size
            surface.blit(small_icon, (x_offset, 10))

            # draw upgrade dots
            level = ing.get("upgrade_level", 0)

            for i in range(3):

                if i < level:
                    color = (255,255,255)   # filled dot
                else:
                    color = (80,80,80)      # empty dot

                pygame.draw.circle(
                    surface,
                    color,
                    (x_offset + 6 + i*10, 45),
                    3
                )

            x_offset -= padding

        scoreText = self.font.render(
            f"{self.currentPoints} / {self.thresholdPoints} points",
            True,
            (0,0,0)
        )

        surface.blit(scoreText, (10, surface.get_height() - 25))

        dist = self.engine.nearest_distance

        if dist is not None:
            feet = round(dist / 20)
            text = self.font.render(
                f"Nearest ingredient {feet} ft away",
                True,
                (0,0,0)
            )
            x = surface.get_width() - text.get_width() - 10
            y = surface.get_height() - text.get_height() - 10
            surface.blit(text, (x, y))

        self.engine.draw(surface)

        if self.engine.flash_timer > 0:            
            flash = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))
            flash.fill((255,255,200))
            flash.set_alpha(100)
            surface.blit(flash, (0,0))
