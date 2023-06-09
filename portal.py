from vector import Vector
import pygame as pg

class Portal:
    def __init__(self, game, rect, velocity=Vector()):
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.portalImages = ['images/bluePortal.png', 'images/animatePortal.png']
        self.currentFrame = 0
        self.active = 0
        self.starF = 0
        self.endF = 1
        self.rect = rect
        self.velocity = velocity
        self.image = pg.transform.rotozoom(pg.image.load(self.portalImages[self.currentFrame]), 0, 0.06)

    def __repr__(self):
        return "Portal(rect={},velocity={})".format(self.rect, self.velocity)
    
    def create_portal(self):
        self.active = 0
        pX, pY = self.game.player.rect.centerx, self.game.player.rect.centery
        if self.game.player.currentAngle == 0:
            cX, cY = 10, -10
            self.velocity = self.settings.portalSpeed * Vector(1, 0)
        elif self.game.player.currentAngle == 180:
            cX, cY = -35, -10
            self.velocity = self.settings.portalSpeed * Vector(-1, 0)
        elif self.game.player.currentAngle == -90:
            cX, cY = -10, 10
            self.velocity = self.settings.portalSpeed * Vector(0, 1)
        else:
            cX, cY = -10, -35
            self.velocity = self.settings.portalSpeed * Vector(0, -1)
        self.rect.left, self.rect.top = pX + cX, pY + cY

    def remove_portal(self, x=350, y=660):
        self.active = 0
        self.rect.left = x
        self.rect.top = y

    def change_frame(self):
        if self.starF <= self.currentFrame < self.endF:
            self.currentFrame += 1
        else:
            self.currentFrame = self.starF

    def check_edges(self):
        self.rect.top = max(73, min(self.settings.screen_height - self.rect.height - 55, self.rect.top))
        if self.settings.m == 0:
            self.rect.left = max(-28, min(self.settings.screen_width - self.rect.width + 48, self.rect.left))
        else:
            self.rect.left = max(-300, min(self.settings.screen_width - self.rect.width + 48, self.rect.left))

    def move(self):
        self.change_frame()
        if self.check_collisions():
            self.velocity = Vector()
            self.active = 1
        if self.rect.top == 73 or self.rect.top == 663 and self.rect.left != 350 and self.rect.left != 400:
            self.active = 1
        if self.active == 0:
            self.rect.left += self.velocity.x
            self.rect.top += self.velocity.y
        self.check_edges()

    def check_collisions(self):
        return False
    
    def draw(self):
        self.image = pg.transform.rotozoom(pg.image.load(self.portalImages[self.currentFrame]), 0, 0.06)
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.check_collisions()
        self.move()
        self.draw()