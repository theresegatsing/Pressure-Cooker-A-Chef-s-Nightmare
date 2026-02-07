import pygame 
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
from selectionScreen import *
RESOLUTION = vec(500,350)
SCALE =2
UPSCALED = RESOLUTION * SCALE

class Game(object):

    def __init__(self, image_path, points):
        self.image_path = image_path
        self.points = points

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(pyVec(UPSCALED))
        start_time = pygame.time.get_ticks()

        running = True
        while running:
            screen.fill((255,255,255))
            pygame.display.flip()

            IngredientDistribution(self.image_path).run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 #in seconds

            if elapsed_time > 120:
                running = False