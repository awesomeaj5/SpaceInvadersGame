# Stephanie Becerra , ID: 888771284
#A.J. Ort, 889672416

from random import randint
from tokenize import group
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers

class Barrier(Sprite):
    color = 255, 0, 0
    black = 0, 0, 0

    def __init__(self, game, rect):
        super().__init__()
        self.screen = game.screen
        self.rect = rect
        self.settings = game.settings
        self.ship_lasers = game.ship_lasers
        self.alien_lasers = game.alien_lasers
        self.hits_left = self.settings.max_barrier_hits
        self.maxwidth = self.settings.screen_width / 10
        # self.settings = game.settings
        # self.image = pg.image.load('images/alien0.bmp')
        # self.rect = self.image.get_rect()
        # self.rect.y = self.rect.height
        # self.x = float(self.rect.x)
        
        
    def hit(self):#pass
        print("barrier has been hit")
        if self.hits_left > 0:
            self.rect.width -= 12
            self.hits_left -= 1
        elif self.hits_left == 0:
            print("barrier destroyed")
            self.kill()

#This was implemented as a fun way to make the barriers a strategy thing to hid behind and recover 
#I wanted to add this since the window version of these setting makes everything so quick that you can't
# accuretly stay under 
    def regrow(self):#pass
        print("barrier has recovered")
        if self.rect.width < self.maxwidth:
            self.rect.width += 12
            self.hits_left += 1
        

        
        

    
    def update(self): 
        self.draw()
    def draw(self): 
        pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 20)
        pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width/6)


class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.ship_lasers = game.ship_lasers
        self.alien_lasers = game.alien_lasers
        self.barriers = Group()
        self.create_barriers()

    def create_barriers(self):     
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
        rects = [pg.Rect(x * 2 * width + 1.5 * width, top, width, height) for x in range(4)]   # SP w  3w  5w  7w  SP
        
        self.barriers.add(Barrier(game=self.game, rect=rects[i])for i in range(4))

    
    
    def check_barrier_collision(self):
        collision = pg.sprite.groupcollide(self.barriers, self.alien_lasers.lasers,False, True)
        ship_collision = pg.sprite.groupcollide(self.barriers, self.ship_lasers.lasers, False, True)
        if collision:
            for barrier in collision:
                barrier.hit()
#part of the side thing to regrow the barrier with player lasers
        #elif ship_collision:
            #for barrier in ship_collision:
                #barrier.regrow()
        

            
    
    def reset(self):
        for barrier in self.barriers:
            barrier.kill()
        self.create_barriers()

    def update(self):
        self.check_barrier_collision()
        for barrier in self.barriers: barrier.update()

    # def draw(self):
    #     for barrier in self.barriers: barrier.draw()

