import pygame
from vector import vec, pyVec
from ingreDistr import IngredientDistribution
from selectionScreen import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 350


class Game(object):

    def __init__(self, image_path, points):

        self.image_path = image_path
        self.points = points

        self.state = IngredientDistribution(image_path, points)

        self.timeLimit = 40
        self.timeLeft = 40.0

        self.finished = False
        self.endScreen = False

        self.timeTaken = 0
        self.score = 0

        self.result = None
        self.timeChange = 0

        self.font = pygame.font.SysFont(None, 22)

        # Buttons
        cx = SCREEN_WIDTH // 2

        self.buttons = {
            "replay": pygame.Rect(cx-80, 240, 160, 35),
            "continue": pygame.Rect(cx-80, 285, 160, 35),
            "menu": pygame.Rect(cx-80, 330, 160, 35)
        }

    def handleEvent(self, event):

        if self.endScreen:

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = event.pos

                # FAILED ROUND
                if self.result == "fail":

                    if self.buttons["replay"].collidepoint(mouse):
                        self.finished = True
                        self.replay = True

                    elif self.buttons["continue"].collidepoint(mouse):
                        self.finished = True
                        self.timeLimit -= self.timeChange

                    elif self.buttons["menu"].collidepoint(mouse):
                        self.finished = True

                # SUCCESS ROUND
                else:

                    if self.buttons["continue"].collidepoint(mouse):
                        self.finished = True
                        self.timeLimit += self.timeChange

                    elif self.buttons["menu"].collidepoint(mouse):
                        self.finished = True

            return

        self.state.handleEvent(event)

    def update(self, seconds):

        if self.endScreen:
            return

        self.timeLeft -= seconds

        if self.timeLeft <= 0:

            self.timeLeft = 0
            self.timeTaken = self.timeLimit
            self.score = self.state.currentPoints

            diff = self.score - self.points
            self.timeChange = abs(diff) / 60

            if self.score >= self.points:
                self.result = "success"
            else:
                self.result = "fail"

            self.endScreen = True
            return

        self.state.update(seconds)

        if all(ing["collected"] for ing in self.state.ingredients):

            self.score = self.state.currentPoints
            self.timeTaken = self.timeLimit - self.timeLeft

            diff = self.score - self.points
            self.timeChange = abs(diff) / 60

            if self.score >= self.points:
                self.result = "success"
            else:
                self.result = "fail"

            self.endScreen = True

    def draw(self, surface):

        if not self.endScreen:

            self.state.draw(surface)

            timerText = self.font.render(
                f"Time: {int(self.timeLeft)}",
                True,
                (0,0,0)
            )

            surface.blit(timerText,(10,10))

        else:

            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            surface.blit(overlay,(0,0))

            cx = surface.get_width() // 2

           #title = self.font.render("Round Complete!",True,(255,255,255))
            timeText = self.font.render(f"Time Taken: {round(self.timeTaken,1)}",True,(255,255,255))
            scoreText = self.font.render(f"Score: {self.score} / {self.points}",True,(255,255,255))

           #surface.blit(title,(cx-90,120))
            surface.blit(timeText,(cx-90,160))
            surface.blit(scoreText,(cx-90,190))

            # FAILURE SCREEN
            if self.result == "fail":

                msg = self.font.render(
                    f"Below target. Next level time -{round(self.timeChange,1)}s",
                    True,(255,200,200)
                )

                surface.blit(msg,(cx-160,215))

                pygame.draw.rect(surface,(120,120,255),self.buttons["replay"])
                pygame.draw.rect(surface,(120,200,120),self.buttons["continue"])
                pygame.draw.rect(surface,(200,120,120),self.buttons["menu"])

                surface.blit(self.font.render("Replay Level",True,(0,0,0)),(cx-50,248))
                surface.blit(self.font.render("Continue",True,(0,0,0)),(cx-35,292))
                surface.blit(self.font.render("Main Menu",True,(0,0,0)),(cx-45,337))

            # SUCCESS SCREEN
            else:

                msg = self.font.render(
                    f"Great! Next level time +{round(self.timeChange,1)}s",
                    True,(200,255,200)
                )

                surface.blit(msg,(cx-140,215))

                pygame.draw.rect(surface,(120,200,120),self.buttons["continue"])
                pygame.draw.rect(surface,(200,120,120),self.buttons["menu"])

                surface.blit(self.font.render("Next Level",True,(0,0,0)),(cx-45,292))
                surface.blit(self.font.render("Main Menu",True,(0,0,0)),(cx-45,337))