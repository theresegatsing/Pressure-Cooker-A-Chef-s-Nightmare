import pygame
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from vector import scale, vec, pyVec, magnitude
from animated import Animated
from constants import *
import random 
 


class GameEngine(object):

    def __init__(self, ingredients):
        self.chef = Player((0,0), "chef.png", (0,0))
        self.chef.animate = True
       
        self.chefSpeed = 100

        self.collidables = ingredients

        #for detecting when the chef changes direction
        self.prev_velocity = vec(0,0)

        self.nearest_distance = None

       

    def draw(self, drawSurface):
        
        self.chef.draw(drawSurface)

            
    def handleEvent(self, event):        

        self.chef.handleEvent(event)        

    
    
    def update(self, seconds):
        self.chef.update(seconds)

        curVelocity = self.chef.velocity

        #detect turning
        if curVelocity[0] != self.prev_velocity[0] or curVelocity[1] != self.prev_velocity[1]:

        
            self.nearest_distance = self.nearestIngredientDistance()
            #if dist != None:
            #    print(f"Nearest ingredient: {feet} feet away")
        
        self.prev_velocity = vec(curVelocity[0], curVelocity[1])

        if self.chef.getPosition()[0] <= 0:
            self.chef.velocity[0] = 0
            self.chef.position[0] = 0
        
        elif self.chef.getPosition()[0] + self.chef.getWidth() > WORLD_SIZE[0]:
            self.chef.position[0] = WORLD_SIZE[0] - self.chef.getWidth() 
            self.chef.velocity[0]= 0
        
        if self.chef.getPosition()[1] <= 0:
            self.chef.velocity[1] = 0
            self.chef.position[1] = 0
        elif self.chef.getPosition()[1] + self.chef.getHeight() > WORLD_SIZE[1]:
            self.chef.position[1] = WORLD_SIZE[1] - self.chef.getHeight()
            self.chef.velocity[1]= 0


        chefRect = self.chef.getCollisionRect()
        for ing in self.collidables:   
            if ing["collected"]:
                continue

            pos = ing["pos"]
            image = ing["image"]

            ingRect = pygame.Rect(
                pos[0],
                pos[1],
                image.get_width(),
                image.get_height()
            )

            if chefRect.colliderect(ingRect):
                ing["collected"] = True

                
                ing["upgrade_level"] += 1
                ing["points"] *= 2

                # upgrade if possible
                if ing["upgrade_level"] < 3:


                    scale = 1 + 0.2 * ing["upgrade_level"]

                    ing["image"] = pygame.transform.rotozoom(
                        ing["image"], 0, scale
                    )

                    new_x = random.randint(0, WORLD_SIZE[0] - ing["image"].get_width())
                    new_y = random.randint(0, WORLD_SIZE[1] - ing["image"].get_height())

                    ing["pos"] = vec(new_x, new_y)
                    ing["collected"] = False


        Drawable.CAMERA_OFFSET = self.chef.getPosition() + self.chef.getSize() /2 -  RESOLUTION /2

        for i in range (2):
             Drawable.CAMERA_OFFSET[i] = max(min(Drawable.CAMERA_OFFSET[i], WORLD_SIZE[i] - RESOLUTION[i]), 
                                              0)
    

    def nearestIngredientDistance(self):
        chef_pos = self.chef.getPosition() + self.chef.getSize() / 2
        min_dist = float('inf')
        
        for ing in self.collidables:
            if ing["collected"]:
                continue

            ing_center = ing["pos"] + vec(
                ing["image"].get_width()/2,
                ing["image"].get_height()/2
            )

            dist = magnitude(ing_center - chef_pos)

            if dist < min_dist:
                min_dist = dist
        
        if min_dist == float('inf'):
            return None
        return min_dist
