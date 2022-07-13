from ast import Global
from multiprocessing import set_forkserver_preload
from turtle import Screen, screensize
import pygame
from pygame import init, sprite
from pygame import mouse
from pygame import color
from pygame.display import update
from pygame.image import tostring
from pygame.locals import *
import sys
from threading import Thread
from castle import Arma, AtaqueEnemigo, Castillo, EstrategiaEnemiga, Juego, Modelo, Nivel, Recurso
from castle_simulation import *

class Drawer:
    WIDTH = 1200
    HEIGHT = 700
    CENTER_X = WIDTH/2
    CENTER_Y = HEIGHT
    PEOPLE_SIZE = [40,20]
    RESOURCE_SIZE = [10,20]
    WEAPON_SIZE = [10,10]
    IS_HOME = True
    
    
   
   
    recursos = {
        'Iron':Recurso('Iron',1000),
        'Wood':Recurso('Wood',1000),
        'Leather':Recurso('Leather',1000),
        'Gold':Recurso('Gold',1000),
       
    }
    
    
    warriors = {
        'SwordSet' : 10,
        'AxeSet' : 3,
        'BowSet' : 4,
        'KnifeSet' : 4,
        'HammerSet' : 5,
        'MagicWandSet' : 5,
        'SpearSet' : 6,
        # 'CatapultSet' : 2
    }
    
   
   
    def __init__(self,state) -> None:
        
        
        self.state = state
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),0,32)
        self.home_image = self.load_image('CastleDefense/UI/sprites/home.jpg')
        self.home_image = pygame.transform.scale(self.home_image,(1200,700))
        self.back_image = self.load_image('CastleDefense/UI/sprites/backImage.jpg')
        self.back_image = pygame.transform.scale(self.back_image,(1200,700))
        
        pygame.init()
        pygame.display.set_caption("Castle Defense")
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.SysFont("Comicsans", 55)
        self.color = (255,255,255)
        self.draw()


    def update(self):
        time = self.clock.tick(60)
        for event in pygame.event.get():
            
            if event.type == QUIT:
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if self.IS_HOME:
                    self.IS_HOME = False
                    self.draw()
                  
            
            elif event.type == MOUSEBUTTONDOWN:
                pass
        
      
        pygame.display.flip()
        pass
        

    def draw_menu(self):
        init_pos = 434
        size = 190
        back_image = self.load_image('CastleDefense/UI/sprites/resourceBack.png')
        back_image =  pygame.transform.scale(back_image,(size,50))
        box = self.load_image('CastleDefense/UI/sprites/boxXL.png')
        box = pygame.transform.scale(box,(self.WIDTH,63))
        pasarTurno = self.load_image('CastleDefense/UI/sprites/pasarTurno.png')
        pasarTurno =  pygame.transform.scale(pasarTurno,(180,50))
        
        opciones = self.load_image('CastleDefense/UI/sprites/opciones.png')
        opciones =  pygame.transform.scale(opciones,(180,50))
        
        self.screen.blit(box,(0,0))
        self.screen.blit(opciones,(7,7))
        self.screen.blit(pasarTurno,(190,7))
        
        font = pygame.font.SysFont("BookmanOldStyle", 20)

        for rec in  self.recursos:
            rec_image = self.load_image ('CastleDefense/UI/sprites/r'+rec+'.png')
            rec_image = pygame.transform.scale(rec_image,(28,28))
            
            amount = font.render(str(self.recursos[rec].cantidad),True,self.color, (0,0,0,0)  )
            amount.set_colorkey((0,0,0), RLEACCEL)
            rec_amount = amount.get_rect()
            w,_ = rec_amount.size
            rec_amount.center = (init_pos+size-w/2-15,32)
            
            
           
            self.screen.blit(back_image,(init_pos,7))
            self.screen.blit(rec_image,(init_pos+12,20))
            self.screen.blit(amount,rec_amount)

            init_pos += size

    def draw_warriors(self):
        init_pos = 0
        size = (80,180)
        font = pygame.font.SysFont("ComicSans", 35,bold= 400)
        color = (33,145,0)
        for warrior in self.warriors:
            if self.warriors[warrior] > 0 :
                
                w_image =  self.load_image ('CastleDefense/UI/sprites/warrior'+warrior+'.png')
                w_image = pygame.transform.scale(w_image,size)
                amount = font.render(str(self.warriors[warrior]),True, color  )
                amount.set_colorkey((0,0,0), RLEACCEL)
                rec_amount = amount.get_rect()
                rec_amount.center = (init_pos+30,self.HEIGHT-200)
                
                self.screen.blit(w_image,(init_pos,self.HEIGHT-180))
                self.screen.blit(amount,rec_amount)
                init_pos += size[0]
        
    def drawEnemies(self):
        init_pos = 780
        size = (80,180)
        
        for i in range(2,7):
            w_image =  self.load_image ('CastleDefense/UI/sprites/enemy'+str(i)+'.png')
            w_image = pygame.transform.scale(w_image,size)
            self.screen.blit(w_image,(init_pos,self.HEIGHT-180))
            init_pos += size[0]
        pass
		
    def draw(self):
        if self.IS_HOME:
            self.screen.blit(self.home_image,(0,0))
        else:
            self.screen.blit(self.back_image,(0,0))
            self.draw_menu()
            self.draw_warriors()
            self.drawEnemies()



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
            
    
   
    
