import pygame
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from vector import vec, pyVec
from animated import Animated

RESOLUTION = vec(500,350)
WORLD_SIZE = vec(1000,700)
SCALE =2
UPSCALED = RESOLUTION * SCALE
import random 

class GameEngine(object):

    def __init__(self):        
        self.chef = Player((0,0), "chef.jpg", (2,1))
        self.chef.animate = True
       
        self.chefSpeed = 100

        #self.collidables = [self.subRainbow, self.waterLily]

       

        self.mouseOffset = vec(0,0)

        self.timer = 5



    def draw(self, drawSurface):
        
        self.chef.draw(drawSurface)
            
    def handleEvent(self, event):        
        
        self.chef.handleEvent(event)        
    
    
    def update(self, seconds):
        self.chef.update(seconds)

        
        self.timer -= seconds

        


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
        #     collision = self.kirby.getCollisionRect().clip(c.getCollisionRect())

            # if collision.width !=0 and collision.height !=0:

            #     if collision.width  < collision.height:
            #         #left /right push
            #         self.kirby.velocity[0] = 0
            #         if self.kirby.getPosition()[0] < c.getPosition()[0]:
            #             #left push
                        
            #             self.kirby.position[0] -= collision.width
            #         else:
            #             #right push
                        
            #             self.kirby.position[0] += collision.width
            #     else:
            #         self.kirby.velocity[1] = 0

            #         if self.kirby.getPosition()[1] < c.getPosition()[1]:
            #             #top push
                        
            #             self.kirby.position[1] -= collision.height
            #         else:
            #             #bottom push
                        
            #             self.kirby.position[1] += collision.height


        Drawable.CAMERA_OFFSET = self.chef.getPosition() + self.chef.getSize() /2 -  RESOLUTION //2 

        for i in range(2):
            Drawable.CAMERA_OFFSET[i] = max(min(Drawable.CAMERA_OFFSET[i], WORLD_SIZE[i] - RESOLUTION[i]), 
                                            0)