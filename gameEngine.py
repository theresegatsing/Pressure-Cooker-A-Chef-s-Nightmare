from cmath import rect

import pygame
from wcwidth import center
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from vector import scale, vec, pyVec, magnitude
from animated import Animated
from constants import *
from orb import Orbs
import random 
 


class GameEngine(object):

    def __init__(self, ingredients, distribution):

        center = vec(WORLD_SIZE[0]//2, WORLD_SIZE[1]//2)
        self.chef = Player(center, "chef.png", (0,0))

        self.chef.animate = False

        self.flash_timer = 0
        self.damage_flash_timer = 0
        self.collected_stack = []  # keeps order of collected ingredients
       
        self.chefSpeed = 100

        self.collidables = ingredients
        self.distribution = distribution

        #for detecting when the chef changes direction
        self.prev_velocity = vec(0,0)

        self.nearest_distance = None

        self.orbs = Orbs()
        self.goblin_hit_cooldown = 0

        
        self.gadget_charges = 0
        self.max_charges = 3

        self.gadget_active = False
        self.gadget_timer = 0
        self.gadget_duration = 7

        self.gadget_unlock_stage = 0  # 0 → none, 1 → 1/3, 2 → 2/3, 3 → full

       

    def draw(self, drawSurface):
        
        self.chef.draw(drawSurface)
        self.orbs.draw(drawSurface)
        if self.gadget_active:
            glow = pygame.Surface(self.chef.getSize(), pygame.SRCALPHA)
            glow.fill((100, 100, 255, 80))
            drawSurface.blit(glow, pyVec(self.chef.getPosition() - Drawable.CAMERA_OFFSET))

        
    
    def handleEvent(self, event):        

        self.chef.handleEvent(event)     

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # press SPACE to activate

                if self.gadget_charges > 0 and not self.gadget_active:
                    self.gadget_active = True
                    self.gadget_timer = self.gadget_duration
                    self.gadget_charges -= 1

    
    
    def update(self, seconds):
        self.chef.update(seconds)
        self.orbs.update(seconds, self.chef)

        if self.goblin_hit_cooldown > 0:
            self.goblin_hit_cooldown -= seconds
        orbs_to_remove = []

        hit_occurred = False  

        for i, orb in enumerate(self.orbs.orbs):

            if hit_occurred:
                break 

            if self.chef.getCollisionRect().colliderect(orb.getCollisionRect()):

                if self.goblin_hit_cooldown <= 0 and not self.gadget_active:

                    if self.collected_stack:
                        entry = self.collected_stack.pop()
                        ing = entry["ingredient"]
                        points_to_remove = entry["points"]

                        if ing["upgrade_level"] > 0:

                            ing["upgrade_level"] -= 1

                            self.distribution.currentPoints -= points_to_remove

                            if self.distribution.currentPoints < 0:
                                self.distribution.currentPoints = 0

                    self.damage_flash_timer = 0.25
                    self.goblin_hit_cooldown = 1.0

                    orbs_to_remove.append(i)

                    hit_occurred = True  

      
        if self.flash_timer > 0:
            self.flash_timer -= seconds
        
        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= seconds

        if magnitude(self.chef.velocity) > 0:
            self.chef.animate = True
        else:
            self.chef.animate = False
            self.chef.frame = 0

        curVelocity = self.chef.velocity

        if magnitude(self.chef.velocity) > 0:
            self.nearest_distance = self.nearestIngredientDistance()

        
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

                self.collected_stack.append({
                    "ingredient": ing,
                    "points": ing["points"]   
                })



                self.flash_timer = 0.15


                self.distribution.currentPoints += ing["points"]
                
                ing["upgrade_level"] += 1
                ing["points"] =  round(ing["points"]/6)

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



        score = self.distribution.currentPoints
        threshold = self.distribution.thresholdPoints

        ratio = score / threshold

        new_stage = 0
        if ratio >= 1:
            new_stage = 3
        elif ratio >= 2/3:
            new_stage = 2
        elif ratio >= 1/3:
            new_stage = 1

        # unlock new charges
        if new_stage > self.gadget_unlock_stage:
            gained = new_stage - self.gadget_unlock_stage
            self.gadget_charges = min(self.gadget_charges + gained, self.max_charges)
            self.gadget_unlock_stage = new_stage


        if self.gadget_active:
            self.gadget_timer -= seconds

            if self.gadget_timer <= 0:
                self.gadget_active = False
                
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
