import pygame
from vector import *
from selectionScreen import SelectionScreen
from constants import *
from ingreDistr import IngredientDistribution
from drawable import Drawable
from mobile import Mobile, Player
from gameEngine import GameEngine
from game import Game

def main():

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(pyVec(UPSCALED))
    drawSurface = pygame.Surface(pyVec(RESOLUTION))
    clock = pygame.time.Clock()

    selectionScreen = SelectionScreen()
    game = None

    state = "selection"
    RUNNING = True

    while RUNNING:

        seconds = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False

            if state == "selection":
                selected_path = selectionScreen.handleEvent(event)

                if selected_path:
                    game = Game(selected_path, 0)
                    state = "game"

            elif state == "game":
                game.handleEvent(event)

        # -------- DRAW / UPDATE --------

        if state == "selection":
            selectionScreen.draw(drawSurface)

        elif state == "game":
            game.update(seconds)
            game.draw(drawSurface)

        pygame.transform.scale(drawSurface, pyVec(UPSCALED), screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()