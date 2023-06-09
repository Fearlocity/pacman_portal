from vector import Vector
import pygame as pg
import time

class Pacman:
    def __init__(self, game, rect, velocity=Vector()):
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.scoreboard = self.game.scoreboard
        self.sounds = self.game.sounds
        self.pacmanImages = ['images/pacman0.png', 'images/pacman1.png', 'images/pacman2.png']
        self.currentFrame = 0
        self.currentAngle = 0
        self.currentDirection = 0
        self.rect = rect
        self.velocity = velocity
        self.player = pg.Rect(300, 100, 25, 25)

        self.image = pg.transform.rotozoom(pg.image.load(self.pacmanImages[self.currentFrame]), self.currentAngle, 0.06)

    def __repr__(self):
        return "Player(rect{}, veolocity{})".format(self.rect, self.velocity)
    
    def change_frame(self):
        if self.velocity == Vector():
            return
        if self.currentDirection == 0:
            if self.currentFrame < len(self.pacmanImages) - 1:
                self.currentFrame += 1
            else:
                self.currentDirection = 1
        else:
            if self.currentFrame > 0:
                self.currentFrame -= 1
            else:
                self.currentDirection = 0
    
    def check_edges(self):
        self.rect.top = max(73, min(self.settings.screen_height - self.rect.height - 80, self.rect.top))
        if 0 <= self.rect.left > self.settings.screen_height:
            self.rect.left = max(-28, min(self.settings.screen_width - self.rect.width + 48, self.rect.left))
        elif self.rect.left < -30:
            self.rect.left = self.settings.screen_width
        elif self.rect.left > self.settings.screen_width:
            self.rect.left = -30
    
    def move_ip(self):
        if self.velocity == Vector():
            return
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        self.check_edges()

    def move(self):
        if self.velocity == Vector():
            return
        
        self.tempX = self.velocity.x
        self.tempY = self.velocity.y

        if self.settings.deaths == 0:
            if not self.check_collisions():
                self.rect.left += self.velocity.x
                self.rect.top += self.velocity.y
            if self.check_collisions():
                self.rect.left -= self.velocity.x
                self.rect.top -= self.velocity.y
            
            if self.tempX != 0 or self.tempY != 0:
                self.change_frame()
            if self.velocity.x > 0:
                self.currentAngle = 0
            elif self.velocity.x < 0:
                self.currentAngle = 180
            elif self.velocity.y > 0:
                self.currentAngle = -90
            else:
                self.currentAngle = 90

            self.check_edges()
    
    def check_ghosts(self):
        if self.settings.deaths == 0:
            if self.rect.colliderect(self.game.blinky.rect) or self.rect.colliderect(self.game.pinky.rect) or self.rect.colliderect(self.game.inky.rect) or self.rect.colliderect(self.game.clyde.rect):
                if self.settings.bluemode == 0:
                    self.pacmanImages = ['images/death0.png', 'images/death1.png', 'image/death2.png', 'images/death3.png', 'images/death4.png']
                    self.currentFrame = 0
                    self.settings.deaths = 1
                else:
                    self.scoreboard.score += 200
                    if self.rect.colliderect(self.game.blinky.rect):
                        self.game.blinky.rect.left = 259
                        self.game.blinky.rect.top = 250
                    if self.rect.colliderect(self.game.pinky.rect):
                        self.game.pinky.rect.left = 259
                        self.game.pinky.rect.top = 305
                    if self.rect.colliderect(self.game.inky.rect):
                        self.game.inky.rect.left = 230
                        self.game.inky.rect.top = 305
                    if self.rect.colliderect(self.game.clyde.rect):
                        self.game.clyde.rect.left = 259
                        self.game.clyde.rect.top = 305
                    self.settings.bluemode = 0
        
        if self.currentFrame == 4:
            self.sounds.pacmanDeath()
            self.rect.left, self.rect.top = 259, 363
            self.game.blinky.rect.left, self.game.blinky.rect.top = 259, 250
            self.game.pinky.rect.left, self.game.pinky.rect.top = 259, 305
            self.game.inky.rect.left, self.game.inky.rect.top = 230, 305
            self.game.clyde.rect.left, self.game.clyde.rect.top = 285, 305
            self.settings.lives -= 1
        
            if self.settings.lives == 0:
                self.game.game_over()
            
            self.pacmanImages = ['images/pacman0.png', 'images/pacman1.png', 'images/pacman2.png']
            self.currentFrame = 0
            self.settings.deaths = 0
            self.velocity = Vector()
            self.game.update()

            if self.settings.lives > 0:
                self.sounds.pacmanIntro()
            
            time.sleep(0.02)

    def check_collisions(self):
        if self.game.bluePortal.active == 1 and self.game.oranPortal.active == 1:
            if self.rect.colliderect(self.game.bluePortal.rect):
                self.sounds.play(4)
                self.game.player.rect.left, self.game.player.rect.top = self.game.oranPortal.rect.left, self.game.oranPortal.rect.top
                self.game.bluePortal.remove_portal()
                self.game.oranPortal.remove_portal(400)
        
        return False

    def draw(self): 
        self.image = pg.transform.rotozoom(pg.image.load(self.pacmanImages[self.currentFrame]), self.currentAngle, 0.06)
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.check_ghosts()
        self.check_collisions()
        self.move()
        self.draw()    