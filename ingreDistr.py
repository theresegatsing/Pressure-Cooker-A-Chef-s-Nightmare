import pygame 

PATH = "C:/Users/gatsi/github/Pressure Cooker/game sprites"

class IngredientDistribution(object):

    def __init__(self, imageCard):
        self.imageCard = imageCard

        self.allMeals = ["burger", "hotdog", "ramen"]

        self.mealPath = ""

        for meal in self.allMeals:
            if meal in self.imageCard:
                self.mealPath = f"{PATH}/{meal}"
                break



    def run(self):
        if self.mealPath == "":
            print("No valid meal found in image card.")
            return
        print(f"Ingredient Distribution for {self.mealPath}")