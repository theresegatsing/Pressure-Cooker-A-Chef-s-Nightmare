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

        self.max_speed = 80        # 🔥 slower top speed
        self.acceleration = 60     # 🔥 smooth turning


        
    def draw(self, screen):
        for orb in self.orbs:
            orb.draw(screen)
        

    def spawn_orb(self, chef):

        chef_pos = chef.getPosition()

        radius = 200

        angle = random.uniform(0, 2 * 3.14159)

        offset = vec(
            radius * pygame.math.Vector2(1, 0).rotate_rad(angle).x,
            radius * pygame.math.Vector2(1, 0).rotate_rad(angle).y
        )

        position = chef_pos + offset

        # clamp to world
        position[0] = max(0, min(position[0], WORLD_SIZE[0] - 50))
        position[1] = max(0, min(position[1], WORLD_SIZE[1] - 50))

        self.orbs.append(Drawable(position, "orb.png"))  # ✅ no offset
        self.positions.append(position)
        self.velocities.append(vec(0, 0))


    def update(self, seconds, chef):

        self.spawn_timer += seconds

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_orb(chef)
            self.spawn_timer -= self.spawn_interval

        deadOrbs = []

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

            # 🔥 smooth acceleration toward chef
            self.velocities[i] += direction * self.acceleration * seconds

            # 🔥 clamp speed (prevents it from getting too fast)
            if magnitude(self.velocities[i]) > self.max_speed:
                self.velocities[i] = (
                    self.velocities[i] / magnitude(self.velocities[i])
                ) * self.max_speed

            # move
            self.positions[i] += self.velocities[i] * seconds
            self.orbs[i].position = self.positions[i]

            # collision
            if chef.getCollisionRect().colliderect(
                self.orbs[i].getCollisionRect()
            ):
                deadOrbs.append(i)

        for index in sorted(deadOrbs, reverse=True):
            del self.orbs[index]
            del self.velocities[index]
            del self.positions[index]