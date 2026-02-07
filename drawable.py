from pygame import image, Surface, SRCALPHA
from os.path import join
from vector import vec, pyVec, rectAdd
from spriteManager import SpriteManager

class Drawable(object):
    def __init__(self, position=vec(0,0), fileName="", offset=None, transparency=False, colorkey=False):
        if fileName != "":
            sm = SpriteManager.getInstance()
            self.image = sm.getSprite(fileName, offset)
            
        
        self.position=vec(*position)
        
    
    def draw(self, drawSurface):        
        drawSurface.blit(self.image, pyVec(self.position))
         
    def getSize(self):
        return vec(*self.image.get_size())    
   
    def getWidth(self):
        return self.getSize()[0]
    
    def getHeight(self):
        return self.getSize()[1]

    def getPosition(self):
        return self.position
    
    def setPosition(self, newPosition):
        self.position = vec(*newPosition)
    
    def getCollisionRect(self):
        return rectAdd(self.getPosition(), self.image.get_rect())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
      