import pygame
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from vector import vec, pyVec, magnitude
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

       

    def draw(self, drawSurface):
        
        self.chef.draw(drawSurface)
            
    def handleEvent(self, event):        

        self.chef.handleEvent(event)        
    
    
    def update(self, seconds):
        self.chef.update(seconds)

        curVelocity = self.chef.velocity

        #detect turning
        if curVelocity != self.prev_velocity:
            dist = self.nearestIngredientDistance()
            

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



        Drawable.CAMERA_OFFSET = self.chef.getPosition() + self.chef.getSize() /2 -  RESOLUTION /2

        for i in range (2):
             Drawable.CAMERA_OFFSET[i] = max(min(Drawable.CAMERA_OFFSET[i], WORLD_SIZE[i] - RESOLUTION[i]), 
                                              0)
    

    def nearestIngredientDistance(self):
        chef_pos = self.chef.getPosition()
        min_dist = float('inf')
        
        for ing in self.collidables:
            if ing["collected"]:
                continue

            dist = magnitude(ing["pos"] - chef_pos)

            if dist < min_dist:
                min_dist = dist
        
        if min_dist == float('inf'):
            return None
        return min_dist
