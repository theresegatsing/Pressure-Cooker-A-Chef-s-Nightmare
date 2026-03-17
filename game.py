import pygame
from vector import vec
from ingreDistr import IngredientDistribution
from selectionScreen import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 350
SCALE = 2


class Game(object):

    def __init__(self, image_path, points):

        self.image_path = image_path
        self.points = points

        self.state = IngredientDistribution(image_path, points)

        self.timeLimit = 120
        self.timeLeft = 120

        self.finished = False
        self.replay = False
        self.endScreen = False

        self.timeTaken = 0
        self.score = 0

        self.result = None
        self.timeChange = 0

        self.font = pygame.font.SysFont(None, 22)

        cx = SCREEN_WIDTH // 2

        # Buttons moved higher
        self.buttons = {
            "replay": pygame.Rect(cx-80, 170, 160, 30),
            "continue": pygame.Rect(cx-80, 205, 160, 30),
            "menu": pygame.Rect(cx-80, 240, 160, 30)
        }

    def handleEvent(self, event):

        if self.endScreen:

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = vec(*event.pos) // SCALE

                if self.result == "fail":

                    if self.buttons["replay"].collidepoint(mouse):
                        self.replay = True
                        self.finished = True

                    elif self.buttons["continue"].collidepoint(mouse):
                        self.timeLimit -= self.timeChange
                        self.finished = True

                    elif self.buttons["menu"].collidepoint(mouse):
                        self.finished = True

                else:

                    if self.buttons["continue"].collidepoint(mouse):
                        self.timeLimit += self.timeChange
                        self.finished = True

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
            self.timeChange = abs(diff) / 40

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
            self.timeChange = abs(diff) / 40

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

            surface.blit(timerText, (10,10))

        else:

            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            surface.blit(overlay,(0,0))

            cx = surface.get_width() // 2

            # INFO TEXT
            timeText = self.font.render(
                f"Time Taken: {round(self.timeTaken,1)}",
                True,(255,255,255)
            )

            scoreText = self.font.render(
                f"Score: {self.score} / {self.points}",
                True,(255,255,255)
            )

            surface.blit(timeText,(cx-80,90))
            surface.blit(scoreText,(cx-80,110))

            if self.result == "fail":

                msg = self.font.render(
                    f"Below target. Next level time -{round(self.timeChange,1)}s",
                    True,(255,200,200)
                )

                surface.blit(msg,(cx-150,135))

                pygame.draw.rect(surface,(120,120,255),self.buttons["replay"])
                pygame.draw.rect(surface,(120,200,120),self.buttons["continue"])
                pygame.draw.rect(surface,(200,120,120),self.buttons["menu"])

                pygame.draw.rect(surface,(255,255,255),self.buttons["replay"],2)
                pygame.draw.rect(surface,(255,255,255),self.buttons["continue"],2)
                pygame.draw.rect(surface,(255,255,255),self.buttons["menu"],2)

                replay_text = self.font.render("Replay Level",True,(0,0,0))
                cont_text = self.font.render("Continue",True,(0,0,0))
                menu_text = self.font.render("Main Menu",True,(0,0,0))

                surface.blit(replay_text,
                    replay_text.get_rect(center=self.buttons["replay"].center))

                surface.blit(cont_text,
                    cont_text.get_rect(center=self.buttons["continue"].center))

                surface.blit(menu_text,
                    menu_text.get_rect(center=self.buttons["menu"].center))

            else:

                msg = self.font.render(
                    f"Great! Next level time +{round(self.timeChange,1)}s",
                    True,(200,255,200)
                )

                surface.blit(msg,(cx-140,135))

                pygame.draw.rect(surface,(120,200,120),self.buttons["continue"])
                pygame.draw.rect(surface,(200,120,120),self.buttons["menu"])

                pygame.draw.rect(surface,(255,255,255),self.buttons["continue"],2)
                pygame.draw.rect(surface,(255,255,255),self.buttons["menu"],2)

                cont_text = self.font.render("Next Level",True,(0,0,0))
                menu_text = self.font.render("Main Menu",True,(0,0,0))

                surface.blit(cont_text,
                    cont_text.get_rect(center=self.buttons["continue"].center))

                surface.blit(menu_text,
                    menu_text.get_rect(center=self.buttons["menu"].center))