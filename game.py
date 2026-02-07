import pygame 
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
RESOLUTION = vec(500,350)
SCALE =2
UPSCALED = RESOLUTION * SCALE

class Game(object):

    def __init__(self, points):
        self.points = points

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(pyVec(UPSCALED))
        start_time = pygame.time.get_ticks()

        running = True
        while running:
            screen.fill((255,255,255))
            pygame.display.flip()

            IngredientDistribution()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 #in seconds

            if elapsed_time > 120:
                running = False