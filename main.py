import pygame
from vector import *
from selectionScreen import SelectionScreen
RESOLUTION = vec(400,200)
SCALE = 2
UPSCALED = RESOLUTION * SCALE


def main():
    
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(pyVec(UPSCALED))
    drawSurface = pygame.Surface(pyVec(RESOLUTION))

    selectionScreen = SelectionScreen()
    RUNNING = True

    while RUNNING:
        selectionScreen.draw(drawSurface)

        pygame.transform.scale(drawSurface,
                               pyVec(UPSCALED),
                               screen)
     
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False
            else:
                selectionScreen.handleEvent(event)
    
    pygame.quit()

if __name__ == '__main__':
    main()


