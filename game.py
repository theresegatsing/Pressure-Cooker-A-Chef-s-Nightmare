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

        self.finished = False  # tells main to return to selection
        self.endScreen = False # shows popup with time taken and score

        self.timeTaken = 0
        self.score = self.points

        self.font = pygame.font.SysFont(None, 18)

    def handleEvent(self, event):
        if self.endScreen:

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.finished = True

            return
        
        self.state.handleEvent(event)

    def update(self, seconds):

        if self.endScreen:
            return

    
        self.timeLeft -= seconds

        if self.timeLeft <= 0:
            self.timeLeft = 0
            self.finished = True
            return

        self.state.update(seconds)

        if all(ing["collected"] for ing in self.state.ingredients):
            self.score = self.points
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
            
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            surface.blit(overlay, (0,0))

            title = self.font.render("Round Complete!", True, (255,255,255))
            timeText = self.font.render(f"Time Taken: {round(self.timeTaken,1)}", True, (255,255,255))
            scoreText = self.font.render(f"Score: {self.score}", True, (255,255,255))
            exitText = self.font.render("Press ESC or Click to go back to Selection Screen", True, (200,200,200))

            cx = surface.get_width() // 2

            surface.blit(title, (cx-110,120))
            surface.blit(timeText,(cx-110,160))
            surface.blit(scoreText,(cx-70,200))
            surface.blit(exitText,(cx-190,250))
    