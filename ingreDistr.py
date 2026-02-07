import pygame 

PATH = "C:/Users/gatsi/github/Pressure Cooker/game sprites"

class IngredientDistribution(object):

    def __init__(self, imageCard):
        self.imageCard = imageCard

        self.allMeals = ["burger", "hot dog", "ramen"]

        self.mealPath = ""

        for meal in self.allMeals:
            if meal in self.imageCard:
                self.mealPath = f"{PATH}/{meal}"
                break



    def run(self):
        pass