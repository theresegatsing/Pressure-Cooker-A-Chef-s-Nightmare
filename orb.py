
import pygame 
from drawable import Drawable
from mobile import Mobile, Player
from vector import vec, pyVec
import random 
from constants import *




class Orbs(object):

    def __init__(self):
    
        

        self.orbs = []   # list of Drawable orbs
        self.velocities = [] # list of velocities for each orb
        self.positions = [] # list of positions for each orb

        self.score = 0

        
    def draw(self, screen):
        for orb in self.orbs:
            orb.draw(screen)
        
    
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = vec(*event.pos) // SCALE

            self.orbs.append(Drawable(position, "orb.png", offset=(0,0)))

            self.velocities.append(vec(random.randint(-100,100), random.randint(-100,100)))
            self.positions.append(position)



    def update(self, seconds, chef):
        deadOrbs = []

        for i in range(len(self.orbs)):

            #Automatically moves the orbs 
            self.positions[i] += self.velocities[i] * seconds
            self.orbs[i].position = self.positions[i]


            #Handles bouncing off walls 
            if self.positions[i][0] <= 0:
                self.velocities[i][0] = - self.velocities[i][0]
                self.positions[i][0] = 0
            
            elif self.positions[i][0] + self.orbs[i].getWidth() > RESOLUTION[0]:
                self.positions[i][0] = RESOLUTION[0] - self.orbs[i].getWidth() 
                self.velocities[i][0]= - self.velocities[i][0]
            
            if self.positions[i][1] <= 0:
                self.velocities[i][1] = - self.velocities[i][1]
                self.positions[i][1] = 0
            elif self.positions[i][1] + self.orbs[i].getHeight() > RESOLUTION[1]:
                self.positions[i][1] = RESOLUTION[1] - self.orbs[i].getHeight()
                self.velocities[i][1]= - self.velocities[i][1]


            #Handles collision with star

            if chef.getCollisionRect().colliderect(self.orbs[i].getCollisionRect()):
                deadOrbs.append(i)
        
        #Removes collided orbs from the lists
        for index in sorted(deadOrbs, reverse=True):
            del self.orbs[index]
            del self.velocities[index]
            del self.positions[index]
