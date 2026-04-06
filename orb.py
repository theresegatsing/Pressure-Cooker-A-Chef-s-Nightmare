import pygame 
from drawable import Drawable
from vector import vec, magnitude
import random 
from constants import *


class Orbs(object):

    def __init__(self):

        self.orbs = []
        self.velocities = []
        self.positions = []

        self.spawn_timer = 0
        self.spawn_interval = 15

        self.max_speed = 90
        self.acceleration = 50   


        
    def draw(self, screen):
        for orb in self.orbs:
            orb.draw(screen)
        

    def spawn_orb(self, chef):

        chef_pos = chef.getPosition()

        radius = 100

        angle = random.uniform(0, 2 * 3.14159)

        offset = vec(
            radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x,
            radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y
        )

        position = chef_pos + offset

        # clamp to world
        position[0] = max(0, min(position[0], WORLD_SIZE[0] - 50))
        position[1] = max(0, min(position[1], WORLD_SIZE[1] - 50))


        orb = Drawable(position, "orb.png")
        orb.image = pygame.transform.scale(orb.image, (32, 32))

        self.orbs.append(orb)  
        self.positions.append(position)
        self.velocities.append(vec(0, 0))


    def update(self, seconds, chef):

        self.spawn_timer += seconds

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_orb(chef)
            self.spawn_timer -= self.spawn_interval


        chef_center = chef.getPosition() + chef.getSize() / 2

        for i in range(len(self.orbs)):

            orb_center = self.positions[i] + vec(
                self.orbs[i].getWidth()/2,
                self.orbs[i].getHeight()/2
            )

            # direction to chef
            direction = chef_center - orb_center
            dist = magnitude(direction)

            if dist != 0:
                direction = direction / dist  # normalize

            desired_velocity = direction * self.max_speed

            self.velocities[i] += (desired_velocity - self.velocities[i]) * 0.1

            #  prevents speed from getting too fast
            if magnitude(self.velocities[i]) > self.max_speed:
                self.velocities[i] = (
                    self.velocities[i] / magnitude(self.velocities[i])
                ) * self.max_speed

            # move
            self.positions[i] += self.velocities[i] * seconds
            self.orbs[i].position = self.positions[i]


            if self.positions[i][0] <= 0:
                self.velocities[i][0] = - self.velocities[i][0]
                self.positions[i][0] = 0
            
            elif self.positions[i][0] + self.orbs[i].getWidth() > WORLD_SIZE[0]:
                self.positions[i][0] = WORLD_SIZE[0] - self.orbs[i].getWidth() 
                self.velocities[i][0]= - self.velocities[i][0]
            
            if self.positions[i][1] <= 0:
                self.velocities[i][1] = - self.velocities[i][1]
                self.positions[i][1] = 0
            elif self.positions[i][1] + self.orbs[i].getHeight() > WORLD_SIZE[1]:
                self.positions[i][1] = WORLD_SIZE[1] - self.orbs[i].getHeight()
                self.velocities[i][1]= - self.velocities[i][1]
