import pygame as pg 
from pygame.sprite import Sprite
from vector import Vector


class Ghosts:
    def __init__(self, game, rect, velocity=Vector()):
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.scoreboard = self.game.scoreboard
        self.sounds = self.game.sounds
        self.ghostImages = ['images/blinky0.png', 'images/blinky1.png', 'images/blinky2.png', 'images/blinky3.png',
                               'images/blinky4.png', 'images/blinky5.png', 'images/blinky6.png', 'images/blinky7.png',
                               'images/run0.png', 'images/run1.png']
        self.currentFrame, self.currentDirection, self.portalPower = 0, 0, 0
        self.startF = 0
        self.endF = 1
        self.rect = rect
        self.velocity = velocity
        self.ghosts = pg.Rect(300, 100, 50, 50)
        self.image = pg.transform.rotozoom(pg.image.load(self.ghostImages[self.currentFrame]), 0, 0.06)

    def __repr__(self):
        return "Enemy(rect={},velocity={})".format(self.rect, self.velocity)
    
    def change_frame(self):
        if self.velocity == Vector():
            return
        if self.startF <= self.currentFrame < self.endF:
            self.currentFrame += 1
        else:
            self.currentFrame = self.startF

    def change_menu_frame(self):
        if self.startF <= self.currentFrame < self.endF:
            self.currentFrame += 1
        else:
            self.currentFrame = self.startF

    def check_edges(self):
        self.rect.top = max(73, min(self.settings.screen_height - self.rect.height - 55, self.rect.top))
        if self.settings.m == 0:
            self.rect.left = max(-28, min(self.settings.screen_width - self.rect.width + 48, self.rect.left))
        else:
            self.rect.left = max(-300, min(self.settings.screen_width - self.rect.width + 48, self.rect.left))
    
    def move(self):
        if self.velocity == Vector():
            return
        if self.scoreboard.level >= 3:
            self.portalPower = 1
        if self.settings.m == 1:
            self.rect.left += self.velocity.x
            self.rect.top += self.velocity.y
            tempX = self.velocity.x
            tempY = self.velocity.y
            if tempX != 0 or tempY != 0:
                self.change_frame()
        else:
            self.change_frame()
            if not self.check_collisions():
                self.rect.left += self.velocity.x
                self.rect.top += self.velocity.y
            if self.check_collisions():
                self.rect.left -= self.velocity.x
                self.rect.top -= self.velocity.y
            if self.settings.bluemode == 0:
                if self.velocity.x > 0:
                    self.startF, self.endF = 2, 3
                elif self.velocity.x < 0:
                    self.startF, self.endF = 0, 1
                elif self.velocity.y > 0:
                    self.startF, self.endF = 4, 5
                else:
                    self.startF, self.endF = 6, 7
            else:
                self.startF, self.endF = 8, 9
        self.check_edges()

    def check_collisions(self):
        if self.game.bluePortal.active == 1 and self.game.oranPortal.active == 1 and self.portalPower == 1:
            if self.rect.colliderect(self.game.bluePortal.rect):
                self.sounds.play_sound(4)
                self.rect.left, self.rect.top = self.game.oranPortal.rect.left, self.game.oranPortal.rect.top
                self.game.bluePortal.remove_portal()
                self.game.oranPortal.remove_portal(400)
            if self.rect.colliderect(self.game.oranPortal.rect):
                self.sounds.play_sound(4)
                self.rect.left, self.rect.top = self.game.bluePortal.rect.left, self.game.bluePortal.rect.top
                self.game.bluePortal.remove_portal()
                self.game.oranPortal.remove_portal(400)


        return False

    def draw(self): 
        self.image = pg.transform.rotozoom(pg.image.load(self.ghostImages[self.currentFrame]), 0, 0.06)
        self.screen.blit(self.image, self.rect)

    def update(self): 
        self.check_collisions()
        self.move()
        self.draw()


class Ghost(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
    def update(self): pass
    def draw(self): pass


class Blinky(Ghost):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
    def update(self): pass
    def draw(self): pass


class Inky(Ghost):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
    def update(self): pass
    def draw(self): pass


class Pinky(Ghost):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
    def update(self): pass
    def draw(self): pass


class Clyde(Ghost):
    def __init__(self, game):
        super().__init__(game=game)
        self.game = game
    def update(self): pass
    def draw(self): pass
