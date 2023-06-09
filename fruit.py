import pygame as pg 
from pygame.sprite import Sprite, Group

class Fruit(Sprite):
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.image = pg.image.load('images/cherry.png')
        self.rect = self.image.get_rect()

        self.rect.left = 259
        self.rect.top = 363
        self.x = float(self.rect.x)

    def check_edges(self):
        return self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0
    
    def update(self): 
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)