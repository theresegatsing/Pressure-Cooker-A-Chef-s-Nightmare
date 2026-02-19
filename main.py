import pygame
from vector import *
from selectionScreen import SelectionScreen
from constants import *
from ingreDistr import IngredientDistribution
from drawable import Drawable
from mobile import Mobile, Player
from gameEngine import GameEngine

def main():
    
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(pyVec(UPSCALED))
    drawSurface = pygame.Surface(pyVec(RESOLUTION))

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    engine = GameEngine(self.ingredients)
    selectionScreen = SelectionScreen()
    
    RUNNING = True

    while RUNNING:
        seconds = clock.tick(60) / 1000 

        selectionScreen.draw(drawSurface)

        pygame.transform.scale(drawSurface,
                               pyVec(UPSCALED),
                               screen)
     
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False
                Drawable.CAMERA_OFFSET = vec(0,0)
            else:
                selectionScreen.handleEvent(event)
    
    pygame.quit()

if __name__ == '__main__':
    main()


