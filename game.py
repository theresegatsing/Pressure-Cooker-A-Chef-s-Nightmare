import pygame 
from vector import vec, pyVec
RESOLUTION = vec(500,350)
SCALE =2
UPSCALED = RESOLUTION * SCALE

class Game(object):

    def __init__(self, points):
        self.points = points

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(pyVec(UPSCALED))
        #drawSurface = pygame.Surface(pyVec(RESOLUTION))
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255,255,255))
            pygame.display.flip()
            clock.tick(60)