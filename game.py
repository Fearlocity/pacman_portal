from random import randint
import pygame as pg
import time
from button import Button
from vector import Vector
from maze import Grid
from pacman import Pacman
from ghosts import Ghosts
from fruit import Fruit
from portal import Portal
from settings import Settings
from sound import Sound
from scoreboard import Scoreboard
import sys


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.width = self.settings.screen_width
        self.height = self.settings.screen_height
        self.screen = pg.display.set_mode((self.width, self.height), 0, 32)
        self.EAT_SOUND, self.GHOST, self.GAME_OVER, self.PORTAL_SOUND, self.PORTAL_CLOSE = 0, 1, 2, 3, 4
        sounds = [{self.EAT_SOUND: 'sounds/eat.ogg',
                   self.GHOST: 'sounds/ghost-normal-move.ogg',
                   self.GAME_OVER: 'sounds/game_over.ogg',
                   self.PORTAL_SOUND: 'sounds/makePortal.ogg',
                   self.PORTAL_CLOSE: 'sounds/closePortal.ogg'}]
        self.sounds = Sound(sounds=sounds, playing=True)
        pg.display.set_caption("Pacman Portal")
        self.font = pg.font.Font('fonts/8-Bit Madness.ttf', 28)
        self.scoreboard = Scoreboard(game=self)
        self.fruit = Fruit(game=self)
        self.mAnimate = Ghosts(self, pg.Rect(self.width, 363, 50, 50), Vector())
        self.mAnimate.ghostImages = ['images/menu0.png', 'images/menu1.png', 'images/menu2.png', 'images/menu3.png',
                                     'images/menu4.png', 'images/menu5.png', 'images/menu6.png']
        
        self.player = Pacman(self, pg.Rect(259, 363, 25, 25), Vector())
        self.blinky = Ghosts(self, pg.Rect(259, 250, 25, 25), Vector())
        self.pinky = Ghosts(self, pg.Rect(259, 305, 25, 25), Vector())
        self.inky = Ghosts(self, pg.Rect(230, 305, 25, 25), Vector())
        self.clyde = Ghosts(self, pg.Rect(285, 305, 25, 25), Vector())
        self.bCount, self.iCount, self.pCount, self.cCount = 0, 0, 0, 0
        self.pinky.ghostImages = ['images/pinky0.png', 'images/pinky1.png', 'images/pinky2.png', 'images/pinky3.png',
                                    'images/pinky4.png', 'images/pinky5.png', 'images/pinky6.png', 'images/pinky7.png',
                                    'images/run0.png', 'images/run1.png']
        self.inky.ghostImages = ['images/inky0.png', 'images/inky1.png', 'images/inky2.png', 'images/inky3.png',
                                    'images/inky4.png', 'images/inky5.png', 'images/inky6.png', 'images/inky7.png',
                                    'images/run0.png', 'images/run1.png']
        self.clyde.ghostImages = ['images/clyde0.png', 'images/clyde1.png', 'images/clyde2.png', 'images/clyde3.png',
                                    'images/clyde4.png', 'images/clyde5.png', 'images/clyde6.png', 'images/clyde7.png',
                                    'images/run0.png', 'images/run1.png']

        self.bluePortal = Portal(self, pg.Rect(350, 660, 25, 25))
        self.oranPortal = Portal(self, pg.Rect(350, 660, 25, 25))
        self.bluePortal.portalImages = ['images/bluePortal.png', 'images/animatePortal.png']
        self.oranPortal.portalImages = ['images/orangePortal.png', 'images/animatePortal.png']
        self.grid = Grid(game=self)

        self.finished = False
        self.mapImage = pg.image.load('images/blank_maze.png')
        self.menuImage = pg.image.load('images/menu.png')
        self.mainClock = pg.time.Clock()

    @staticmethod
    def wait_for_event(self):
        key_pressed = False
        while not key_pressed:
            for e in pg.event.get():
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.game_over()
                elif e.type == pg.KEYDOWN:
                    key_pressed = True

    def handle_events(self, event):
        e_type = event.type
        movement = {pg.K_a: Vector(-1, 0), pg.K_d: Vector(1, 0), pg.K_w: Vector(0, -1), pg.K_s: Vector(0, 1)}
        translate = {pg.K_LEFT: pg.K_a, pg.K_RIGHT: pg.K_d, pg.K_UP: pg.K_w, pg.K_DOWN: pg.K_s}
        left_right_up_down = (pg.K_LEFT, pg.K_a, pg.K_RIGHT, pg.K_d, pg.K_UP, pg.K_w, pg.K_DOWN, pg.K_s)
        x_z = (pg.K_x, pg.K_z)

        if e_type == pg.KEYDOWN or e_type == pg.KEYUP:
            k = event.key
            if k == pg.K_m and e_type == pg.KEYUP:
                pg.mixer.music.stop()
            elif k in x_z:
                if e_type == pg.KEYDOWN:
                    pass
                elif e_type == pg.KEYUP:
                    pass
            elif k in left_right_up_down:
                if k in translate.keys():
                    k = translate[k]
                self.player.velocity = self.settings.pacmanSpeed * movement[k]
            elif k == pg.K_q:
                self.bluePortal.create_portal()
                self.sounds.play(3)
                pass
            elif k == pg.K_e:
                self.oranPortal.create_portal()
                self.sounds.play(3)
                pass
        elif e_type == pg.QUIT or (e_type == pg.KEYUP and pg.event.key == pg.K_ESCAPE):
            self.finished = True

    def update(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.mapImage, (0, 46))

        text = self.font.render(f'Score: {self.scoreboard.score}', True, self.settings.WHITE, self.settings.BLACK)
        textRect = text.get_rect()
        textRect.center = (70, 25)
        self.screen.blit(text, textRect)

        text2 = self.font.render(f'Level: {self.scoreboard.level}', True, self.settings.WHITE, self.settings.BLACK)
        textRect2 = text2.get_rect()
        textRect2.center = (500, 25)
        self.screen.blit(text2, textRect2)

        text3 = self.font.render(f'Lives: {self.settings.lives}', True, self.settings.WHITE, self.settings.BLACK)
        textRect3 = text3.get_rect()
        textRect3.center = (70, 675)
        self.screen.blit(text3, textRect3)

        self.grid.update()
        self.player.update()
        self.bluePortal.update()
        self.oranPortal.update()

        if self.settings.lives == 0:
            self.settings.gameOver = 1
            self.settings.lives = 3

            self.scoreboard.update_highscore()

            self.scoreboard.score = 0
            self.scoreboard.level  = 1
            self.grid.reset_grid()

            self.player.rect.left, self.player.rect.top = 259, 363
            self.blinky.rect.left, self.blinky.rect.top = 259, 250
            self.pinky.rect.left, self.pinky.rect.top = 259, 305
            self.inky.rect.left, self.inky.rect.top = 230, 305
            self.clyde.rect.left, self.clyde.rect.top = 285, 305
            self.screen.fill(self.settings.bg_color)
            self.screen.blit(self.mapImage, (0, 46))
            self.screen.blit(self.gameOver, self.gameOverRect)
            self.menu()

        else:
            if self.scoreboard.score % 700 == 0 or self.scoreboard.score % 1700 == 0: pass
                # self.fruit.update()
            if self.mainClock.get_time() % randint(1, 40) == 0:
                self.bCount = randint(1, 4)
                if self.bCount == 1:
                    self.blinky.velocity = self.settings.enemySpeed * Vector(1, 0)
                elif self.bCount == 2:
                    self.blinky.velocity = self.settings.enemySpeed * Vector(0, 1)
                elif self.bCount == 3:
                    self.blinky.velocity = self.settings.enemySpeed * Vector(-1, 0)
                else:
                    self.blinky.velocity = self.settings.enemySpeed * Vector(0, -1)
            self.blinky.update()
            if self.mainClock.get_time() % randint(1, 40) == 0:
                self.pCount = randint(1, 4)
                if self.pCount == 1:
                    self.pinky.velocity = self.settings.enemySpeed * Vector(1, 0)
                elif self.pCount == 2:
                    self.pinky.velocity = self.settings.enemySpeed * Vector(0, 1)
                elif self.pCount == 3:
                    self.pinky.velocity = self.settings.enemySpeed * Vector(-1, 0)
                else:  
                    self.pinky.velocity = self.settings.enemySpeed * Vector(0, -1)
            self.pinky.update()
            if self.mainClock.get_time() % randint(1, 40) == 0:
                self.iCount = randint(1, 4)
                if self.iCount == 1:
                    self.inky.velocity = self.settings.enemySpeed * Vector(1, 0)
                elif self.iCount == 2:
                    self.inky.velocity = self.settings.enemySpeed * Vector(0, 1)
                elif self.iCount == 3:
                    self.inky.velocity = self.settings.enemySpeed * Vector(-1, 0)
                else: 
                    self.inky.velocity = self.settings.enemySpeed * Vector(0, -1)
            self.inky.update()
            if self.mainClock.get_time() % randint(1, 40) == 0:
                self.cCount = randint(1, 4)
                if self.cCount == 1:
                    self.clyde.velocity = self.settings.enemySpeed * Vector(1, 0)
                elif self.cCount == 2:
                    self.clyde.velocity = self.settings.enemySpeed * Vector(0, 1)
                elif self.cCount == 3:
                    self.clyde.velocity = self.settings.enemySpeed * Vector(-1, 0)
                else:  
                    self.clyde.velocity = self.settings.enemySpeed * Vector(0, -1)
            self.clyde.update()
            pg.display.update()

    def menu(self):
        self.m = 1
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load('sounds/PacmanRemix.mp3')
            pg.mixer.music.play()
        self.screen.blit(self.menuImage, (0, 0))
        self.mAnimate.update()

        play_button = Button(self.screen, "Play")
        play_button.rect.top += 200
        play_button.prep_msg("Play")

        hScore_button = Button(self.screen, "Highscores")
        hScore_button.rect.top += 250
        hScore_button.prep_msg("Highscores")

        pg.display.update()
        play_button.draw_button()
        hScore_button.draw_button()

        blinkC, pinkC, inkyC, clydeC = (249, 0, 0), (249, 141, 224), (5, 249, 249), (249, 138, 13)
        text0 = self.font.render('Blinky', True, blinkC, (0, 0, 0))
        text1 = self.font.render('Pinky', True, pinkC, (0, 0, 0))
        text2 = self.font.render('Inky', True, inkyC, (0, 0, 0))
        text3 = self.font.render('Clyde', True, clydeC, (0, 0, 0))
        text4 = self.font.render('How High Can You Score?', True, (249, 241, 0), (0, 0, 0))
        textRect0, textRect1, textRect2, textRect3, textRect4 = text0.get_rect(), text1.get_rect(), text2.get_rect(), text3.get_rect(), text4.get_rect()
        textRect0.center, textRect1.center, textRect2.center, textRect3.center, textRect4.center = (275, 450), (275, 450), (275, 450), (275, 450), (275, 450)

        key_pressed = False
        count = 0
        temp = -1
        itemp = 0

        blinky = self.blinky
        pinky = self.pinky
        inky = self.inky
        clyde = self.clyde

        blinky.rect.left, blinky.rect.top = 260, 410
        pinky.rect.left, pinky.rect.top = 260, 410
        inky.rect.left, inky.rect.top = 260, 410
        clyde.rect.left, clyde.rect.top = 260, 410

        while not key_pressed:
            itemp += 1
            if count == 150:
                temp *= -1
                count = 0
            count += 1

            self.mAnimate.velocity = self.settings.enemySpeed * Vector(1 * temp, 0)
            self.screen.blit(self.menuImage, (0, 0))
            if itemp < 250:
                if count < 50 and self.settings.gameOver == 1:
                    self.screen.blit(self.gameOver, self.gameOverRect)
                elif self.settings.gameOver == 1:
                    self.settings.gameOver = 0
                if self.mAnimate.velocity == self.settings.enemySpeed * Vector(-1, 0):
                    self.mAnimate.rect.left = self.mAnimate.rect.left
                    self.mAnimate.startF, self.mAnimate.endF = 3, len(self.mAnimate.ghostImages) - 1
                else:
                    self.mAnimate.startF, self.mAnimate.endF = 0, 2
                    self.screen.blit(text4, textRect4)

                self.mAnimate.update()

            if 250 <= itemp <= 310:
                self.screen.blit(text0, textRect0)
                blinky.change_menu_frame()
                blinky.update()
            elif 310 <= itemp <= 365:
                self.screen.blit(text1, textRect1)
                pinky.change_menu_frame()
                pinky.update()
            elif 345 <= itemp <= 400:
                self.screen.blit(text2, textRect2)
                inky.change_menu_frame()
                inky.update()
            elif 400 <= itemp <= 450:
                self.screen.blit(text3, textRect3)
                clyde.change_menu_frame()
                clyde.update()
            elif itemp >= 450:
                itemp = 0
                temp *= -1

            play_button.draw_button()
            hScore_button.draw_button()
            pg.display.update()
            for e in pg.event.get():
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.game_over()
                elif e.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    play_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
                    score_clicked = hScore_button.rect.collidepoint(mouse_x, mouse_y)
                    if play_clicked:
                        key_pressed = True
                    if score_clicked:
                        self.scoreboard.highscore_menu()
                else:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    play_hover = play_button.rect.collidepoint(mouse_x, mouse_y)
                    score_hover = hScore_button.rect.collidepoint(mouse_x, mouse_y)
                    if play_hover:
                        play_button.text_color = (255, 255, 255)
                        play_button.prep_msg("Play")
                        play_button.draw_button()
                    else:
                        play_button.text_color = play_button.temp_color
                        play_button.prep_msg("Play")
                        play_button.draw_button()
                    if score_hover:
                        hScore_button.text_color = (255, 255, 255)
                        hScore_button.prep_msg("Highscores")
                        hScore_button.draw_button()
                    else:
                        hScore_button.text_color = hScore_button.temp_color
                        hScore_button.prep_msg("Highscores")
                        hScore_button.draw_button()
            time.sleep(0.02)
        self.m = 0  
        self.blinky.rect.left, self.blinky.rect.top = 259, 250
        self.pinky.rect.left, self.pinky.rect.top = 259, 305
        self.inky.rect.left, self.inky.rect.top = 230, 305
        self.clyde.rect.left, self.clyde.rect.top = 285, 305
        self.play()

    def game_over(self):
        self.gameOver = self.font.render('Game Over... Play Again?', True, self.settings.WHITE, self.settings.BLACK)
        self.gameOverRect = self.gameOver.get_rect()
        self.gameOverRect.center = (275, 325)
        self.screen.blit(self.gameOver, self.gameOverRect)
        self.sounds.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        pg.mixer.music.load(self.sounds.bg_music)
        pg.mixer.music.play(1, 0.0)
        while not self.finished:
            for event in pg.event.get():
                self.handle_events(event)

            self.update()
            while pg.mixer.music.get_busy():
                time.sleep(0.02)
            time.sleep(0.02)
            self.mainClock.tick(self.settings.FPS)
        self.game_over()

def main():
    g = Game()
    g.menu()


if __name__ == '__main__':
    main()

