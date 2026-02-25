import pygame 
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
from selectionScreen import *



class Game(object):

    def __init__(self, image_path, points):

        self.image_path = image_path
        self.points = points

        self.state = IngredientDistribution(image_path)

        self.timeLimit = 60.0 # seconds
        self.timeLeft = 60.0
        self.finished = False

        self.endScreen = False
        self.timeTaken = 0

        self.font = pygame.font.SysFont(None, 18)

    def handleEvent(self, event):
        self.state.handleEvent(event)

    def update(self, seconds):

        if self.finished:
            return

        self.timeLeft -= seconds

        if self.timeLeft <= 0:
            self.timeLeft = 0
            self.finished = True
            return

        self.state.update(seconds)

        if all(ing["collected"] for ing in self.state.ingredients):
            self.finished = True

        if self.finished and not self.endScreen:
            self.timeTaken = self.timeLimit - self.timeLeft
            self.endScreen = True

    def draw(self, surface):

        if not self.endScreen:

            self.state.draw(surface)

            timerText = self.font.render(
                f"Time: {int(self.timeLeft)}",
                True,
                (0,0,0)
            )
            surface.blit(timerText, (10, 10))

        else:
            surface.fill((255,255,255))

            timeText = self.font.render(
                f"Time Taken: {round(self.timeTaken,1)}",
                True,
                (0,0,0)
            )

            scoreText = self.font.render(
                f"Score: {self.points}",
                True,
                (0,0,0)
            )

            surface.blit(timeText, (RESOLUTION[0]//2 - 80, 120))
            surface.blit(scoreText, (RESOLUTION[0]//2 - 50, 160))