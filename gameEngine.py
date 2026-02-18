import pygame
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from vector import vec, pyVec
from animated import Animated
from constants import *
import random 

class GameEngine(object):

    def __init__(self, ingredients):
        self.chef = Player((0,0), "chef.png", (0,0))
        self.chef.animate = True
       
        self.chefSpeed = 100

        self.collidables = ingredients

       

       #self.mouseOffset = vec(0,0)


    def draw(self, drawSurface):
        
        self.chef.draw(drawSurface)
            
    def handleEvent(self, event):        

        self.chef.handleEvent(event)        
    
    
    def update(self, seconds):
        self.chef.update(seconds)


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


     # for c in self.collidables:
     #      collision = self.chef.getCollisionRect().clip(c.getCollisionRect())

      #     if collision.width !=0 and collision.height !=0:
     #          self.collidables.remove(c)


        Drawable.CAMERA_OFFSET = self.chef.getPosition() + self.chef.getSize() /2 -  RESOLUTION /2

        for i in range (2):
             Drawable.CAMERA_OFFSET[i] = max(min(Drawable.CAMERA_OFFSET[i], WORLD_SIZE[i] - RESOLUTION[i]), 
                                              0)
        