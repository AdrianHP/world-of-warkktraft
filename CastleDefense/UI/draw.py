from ast import Global
from multiprocessing import set_forkserver_preload
import pygame
from pygame import init, sprite
from pygame import mouse
from pygame import color
from pygame.display import update
from pygame.image import tostring
from pygame.locals import *
import sys
from threading import Thread







class Drawer:
    WIDTH = 1300
    HEIGHT = 700
    CENTER_X = WIDTH/2
    CENTER_Y = HEIGHT
    PEOPLE_SIZE = [40,20]
    RESOURCE_SIZE = [10,20]
    WEAPON_SIZE = [10,10]
    IS_HOME = True
   
   
    recursos = {
        'Sword':Recurso('Iron',1000)
    }
   
   
    def __init__(self,state) -> None:
        
        
        self.state = state
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),0,32)
        self.home_image = self.load_image('CastleDefense/UI/sprites/home.jpg')
        self.home_image = pygame.transform.scale(self.home_image,(1300,700))
        self.back_image = self.load_image('CastleDefense/UI/sprites/backImage.jpg')
        self.back_image = pygame.transform.scale(self.back_image,(1300,700))
        
        pygame.display.set_caption("Castle Defense")
        self.clock = pygame.time.Clock()
    


    def update(self):
        time = self.clock.tick(60)
        for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if self.IS_HOME:
                    self.IS_HOME = False
                  
            
            elif event.type == MOUSEBUTTONDOWN:
                pass
        
        self.draw()
        pygame.display.flip()
        pass
        

    def drawUpMenu(self):
        pass

    def draw(self):
        if self.IS_HOME:
            self.screen.blit(self.home_image,(0,0))
        else:
            self.screen.blit(self.back_image,(0,0))



    def load_image(self,filename, transparent=False):
        image = pygame.image.load(filename)
        # image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image
    


def main():
    d = Drawer('')
    while True:
        d.update()
    
main()            
            
    
   
    
