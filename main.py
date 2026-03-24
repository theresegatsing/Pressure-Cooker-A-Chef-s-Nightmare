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
        drawSurface.fill((0,0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False

            if state == "selection":
                result = selectionScreen.handleEvent(event)

                if result:
                    image_path, points = result
                    game = Game(image_path, points)
                    state = "game"

            elif state == "game":
                game.handleEvent(event)


        if state == "selection":
            selectionScreen.draw(drawSurface)

        elif state == "game":

            game.update(seconds)

            if game.finished:
                if getattr(game, 'next_level', False):
                    # Go to next level
                    next_level = game.level + 1
                    # Here, you can select the next game parameters
                    image_path, points = LevelCards.get_cards(next_level)
                    game = Game(image_path, points)
                    state = "game"
                else:
                    game = None
                    Drawable.CAMERA_OFFSET = vec(0,0)
                    state = "selection"
                    continue

            game.draw(drawSurface)

        pygame.transform.scale(drawSurface, pyVec(UPSCALED), screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()