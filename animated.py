from drawable import Drawable 
from vector import vec 
from spriteManager import SpriteManager

class Animated(Drawable):
    def __init__(self, position = vec(0,0), fileName = "", offset = None):
        super() .__init__(position, fileName, offset)

        self.animationTimer = 0
        self.frame =0
        self.animate = False
        self.framesPerSecond = 10
        self.nFrame = 4
        self.row = 1


    
    def update(self, seconds):
        if self.animate:
            
            self.animationTimer += seconds
            
            if self.animationTimer >= 1 / self.framesPerSecond:
                self.frame += 1
                self.frame %= self.nFrame
                self.animationTimer -= 1/ self.framesPerSecond
                self.image = SpriteManager.getInstance().getSprite(self.fileName, (self.frame, self.row))

   
