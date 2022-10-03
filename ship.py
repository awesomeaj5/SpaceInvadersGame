# Stephanie Becerra , ID: 888771284
#A.J. Ort, 889672416

import pygame as pg
from pygame.sprite import Sprite
from laser import Lasers
from game_functions import clamp
from vector import Vector
from sys import exit
from timer import Timer

class Ship(Sprite):

    ship_explosion_images = [pg.image.load(f'images/frame_{n}.png') for n in range(15)]


    def __init__(self, game):
        super().__init__()
        self.dieing = False
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.ships_left = game.settings.ship_limit  
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.posn = self.center_ship()    # posn is the centerx, bottom of the rect, not left, top
        self.vel = Vector()

        
        self.timer_explosion = Timer(image_list=Ship.ship_explosion_images, is_loop=False)
        
        # self.lasers = Lasers(settings=self.settings)
        self.lasers = game.ship_lasers

        self.alien_lasers = game.alien_lasers

        # self.lasers = lasers
        self.shooting = False
        self.lasers_attempted = 0
    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)
    def reset(self):
        self.vel = Vector()
        self.posn = self.center_ship()
        self.lasers.reset()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y
    def die(self):
# # TODO: reduce the ships_left, 
# #       reset the game if ships > 0
# #       game_over if the ships == 0
        if not self.dieing:
            self.ships_left -= 1
            print(f'Ship is dead! Only {self.ships_left} ships left')
        
            if self.ships_left > 0:
                self.dieing = True
                self.game.reset()  
            else: 
                self.dieing = True
                self.game.game_over()  
            
            

    def update(self):
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(game=self.game, x = self.rect.centerx, y=self.rect.top)
        self.lasers.update()
        self.draw()
    def draw(self):
        if self.dieing:
            images = self.timer_explosion.image()
            rect = images.get_rect()
            rect.left, rect.top = self.rect.left, self.rect.top
            self.screen.blit(images, rect)
            if self.timer_explosion.is_expired():
                self.dieing = False 
                self.timer_explosion.reset()
                
        else:
            self.screen.blit(self.image,self.rect)
