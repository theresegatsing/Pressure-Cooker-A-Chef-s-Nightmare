from drawable import Drawable
from vector import vec, magnitude, scale
from pygame.locals import *

class Mobile(Drawable):
    def __init__(self, position, fileName="", offset=None, maxSpeed=100, transparency=False, colorkey=False):
        super().__init__(position, fileName, offset, transparency, colorkey)
        self.velocity = vec(0,0)
        self.maxSpeed = maxSpeed
    
    def update(self, seconds):
        if magnitude(self.velocity) > self.maxSpeed:
            self.velocity = scale(self.velocity, self.maxSpeed)

        self.position += self.velocity * seconds



class Player(Mobile):
    def __init__(self, position, fileName="", offset=None, maxSpeed=100, transparency=False, colorkey=False):
        super().__init__(position, fileName, offset, maxSpeed, transparency, colorkey)
        self.speed = 100

        self.keyMap = {
            K_UP    : False,
            K_DOWN  : False,
            K_RIGHT : False,
            K_LEFT  : False
        }

    
    def handleEvent(self, event):
        if event.type in (KEYDOWN, KEYUP) and event.key in self.keyMap.keys():
            self.keyMap[event.key] = event.type == KEYDOWN
    
    def update(self, seconds):
        if self.keyMap[K_LEFT] or self.keyMap[K_RIGHT]:
            if self.keyMap[K_LEFT]:
                self.velocity[0] = -self.speed
            else:
                self.velocity[0] = self.speed
        else:
            self.velocity[0] = 0
        if self.keyMap[K_UP] or self.keyMap[K_DOWN]:
            if self.keyMap[K_UP]:
                self.velocity[1] = -self.speed
            else:
                self.velocity[1] = self.speed
        else:
            self.velocity[1] = 0
        
        super().update(seconds)

