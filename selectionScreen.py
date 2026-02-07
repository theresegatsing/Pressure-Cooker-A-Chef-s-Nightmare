import pygame 
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from PIL import Image


pygame.init()
#font = pygame.font.Font("Lonely Study.otf", 14)
font = pygame.font.Font(None, 14)

class SelectionScreen(object):
    def __init__(self):
        
        self.background = Drawable((0,0), "Selection Screen background.jpg")
        self.background.image = pygame.transform.smoothscale( self.background.image, (500, 350))
        self.burgerCard = Drawable((40,40),  "burger card.png")
        self.burgerCard.image = pygame.transform.smoothscale(self.burgerCard.image, (150, 200))
    
    def draw(self, surface):
        
        surface.fill((0,0,0))
        
        self.background.draw(surface)
        self.burgerCard.draw(surface)
        text = (" 2100 points . A burger is a popular meal that originated in Germany, specifically in the city of Hamburg. "
        "It was inspired by the Hamburg steak and later became widely known after being introduced in the United States.")
        self.render_multiline_text(
        surface,
        text,
        font,
        (0, 0, 0),         # black color
        (60, 90 + 110 + 5), # x = same as card, y = card y + card height + small padding
        150                  # max width = card width
        )


    
    def handleEvent(self, event):
        
        pass

    def render_multiline_text(self, surface, text, font, color, pos, max_width):
        words = text.split(' ')
        lines = []
        line = ''

        for word in words:
            test_line = line + word + ' '
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)

        x, y = pos
        for line in lines:
            text_surface = font.render(line.strip(), True, color)
            surface.blit(text_surface, (x, y))
            y += font.get_linesize()  # move down for next line
