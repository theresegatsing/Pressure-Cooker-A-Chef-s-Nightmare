import pygame 
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
from selectionScreen import *



class Game(object):

    def __init__(self, image_path, points):

        self.image_path = image_path
        self.points = points

        self.state = IngredientDistribution(image_path)

        # TIMER
        self.timeLimit = 30.0   # seconds
        self.timeLeft = 30.0
        self.finished = False

        self.font = pygame.font.SysFont(None, 28)

    # ------------------
    def handleEvent(self, event):
        self.state.handleEvent(event)

    # ------------------
    def update(self, seconds):

        if self.finished:
            return

        self.timeLeft -= seconds

        if self.timeLeft <= 0:
            self.timeLeft = 0
            self.finished = True
            return

        self.state.update(seconds)

    # ------------------
    def draw(self, surface):

        self.state.draw(surface)

        # DRAW TIMER (top-left)
        timerText = self.font.render(
            f"Time: {int(self.timeLeft)}",
            True,
            (0,0,0)
        )
        surface.blit(timerText, (10, 10))