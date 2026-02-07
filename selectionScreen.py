import pygame 
from drawable import Drawable
from mobile import Mobile, Player
from os.path import join
from PIL import Image
from card import Card 
import random 
from vector import vec

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 350

CARD_WIDTH = 150
CARD_HEIGHT = 200
CARD_GAP = 20
TEXT_PADDING = 5

pygame.init()
#font = pygame.font.Font("Lonely Study.otf", 14)
font = pygame.font.Font(None, 14)

class SelectionScreen(object):
    def __init__(self):
        
        self.background = Drawable((0,0), "Selection Screen background.jpg")
        self.background.image = pygame.transform.smoothscale( self.background.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.allCards = [
            Card("burger card.png", 
                 "A burger is a popular meal that originated in Germany, specifically in the city of Hamburg. "
                "It was inspired by the Hamburg steak and later became widely known after being introduced in the United States." , 
                2100),
        
            Card("hotdog card.png", 
                 "A hot dog is a popular meal that originated in Germany, specifically from Frankfurt and Vienna. It was inspired by traditional German sausages (frankfurters and wieners) and later became widely known after being introduced in the United States" , 
                 2000),
            
            Card("ramen card.png",
                 "Ramen is a popular noodle dish that originated in Japan. It was inspired by Chinese wheat noodles and later evolved into a staple of Japanese cuisine, becoming widely known around the world.",
                 2300)
        ]

        self.selectedCards = random.sample(self.allCards, 3)
        self.position_cards_centered()

    
    def position_cards_centered(self):
        total_width = (
            len(self.selectedCards) * CARD_WIDTH
            + (len(self.selectedCards) - 1) * CARD_GAP
        )

        start_x = (SCREEN_WIDTH - total_width) // 2
        y = 40

        for i, card in enumerate(self.selectedCards):
            x = start_x + i * (CARD_WIDTH + CARD_GAP)
            card.drawable.position = vec(x, y)


    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.background.draw(surface)

        for card in self.selectedCards:
            card.drawable.draw(surface)

            text_y = card.drawable.position.y + CARD_HEIGHT + TEXT_PADDING
            text_x = card.drawable.position.x

            self.render_multiline_text(
                surface,
                card.description,
                font,
                (0, 0, 0),
                (text_x, text_y),
                CARD_WIDTH
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
