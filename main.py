import pygame
from vector import *
from selectionScreen import SelectionScreen
from constants import *
from ingreDistr import IngredientDistribution
from drawable import Drawable
from mobile import Mobile, Player
from gameEngine import GameEngine
from game import Game
from levelCards import LevelCards
from soundManager import SoundManager


def main():

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(pyVec(UPSCALED))
    drawSurface = pygame.Surface(pyVec(RESOLUTION))
    clock = pygame.time.Clock()

    selectionScreen = SelectionScreen(1)
    game = None

    state = "selection"
    RUNNING = True

    sm = SoundManager.getInstance() 



    next_time_limit = None

    while RUNNING:

        seconds = clock.tick(60) / 1000
        drawSurface.fill((0,0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False

            if state == "selection":
                result = selectionScreen.handleEvent(event)

                if result:
                    image_path, points = result
                    game = Game(image_path, points)
                    if next_time_limit is not None:

                        game.timeLimit = next_time_limit
                        game.timeLeft = next_time_limit
                        next_time_limit = None

                    state = "game"

            elif state == "game":
                game.handleEvent(event)


        if state == "selection":
            selectionScreen.draw(drawSurface)

        elif state == "game":

            game.update(seconds)


            if game.finished:
                if getattr(game, 'next_level', False):
                    # Go back to selection screen for the next level
                    next_level = game.level + 1
                    selectionScreen = SelectionScreen(next_level)  # pass level to constructor
                    next_time_limit = game.next_time_limit

                    state = "selection"
                else:
                    # normal finish → go back to first level selection or menu
                    selectionScreen = SelectionScreen(1)  # or keep same level
                    state = "selection"
                
                game = None
                Drawable.CAMERA_OFFSET = vec(0,0)
                continue
            game.draw(drawSurface)

        pygame.transform.scale(drawSurface, pyVec(UPSCALED), screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()