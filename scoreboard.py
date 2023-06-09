import pygame as pg 
# import pygame.font

class Scoreboard:
    def __init__(self, game):
        self.game = game
        
        self.score = 0
        self.level = 1
        self.high_score = 0
        self.topScores = []

        f = open('highscores.txt', 'r')
        f1 = f.readlines()
        for s in f1:
            self.topScores.append(int(s))
        f.close()
        self.topScores.sort(reverse=True)
        
        self.settings = game.settings
        self.font = game.font
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None
        self.prep_score()

    def update_highscore(self):
        self.topScores.append(self.score)
        f = open('highscores.txt', 'a')
        f.write(f'\n{self.score}')
        f.close()
        self.topScores.sort(reverse=True)

    def highscore_menu(self):
        self.h = 1  # highscores is on

        self.screen.fill(self.settings.bg_color)
        text = self.font.render('High Scores:', True, (249, 241, 0), (0, 0, 0))
        text0 = self.font.render(f'#1: {self.topScores[0]}', True, (249, 241, 0), (0, 0, 0))
        text1 = self.font.render(f'#2: {self.topScores[1]}', True, (249, 241, 0), (0, 0, 0))
        text2 = self.font.render(f'#3: {self.topScores[2]}', True, (249, 241, 0), (0, 0, 0))
        text3 = self.font.render(f'#4: {self.topScores[3]}', True, (249, 241, 0), (0, 0, 0))
        text4 = self.font.render(f'#5: {self.topScores[4]}', True, (249, 241, 0), (0, 0, 0))
        textRect, textRect0, textRect1, textRect2, textRect3, textRect4 = text.get_rect(), text0.get_rect(), text1.get_rect(), text2.get_rect(), text3.get_rect(), text4.get_rect()
        textRect.center, textRect0.center, textRect1.center, textRect2.center, textRect3.center, textRect4.center,  = (285, 150), (285, 200), (285, 250), (285, 300), (285, 350), (285, 400)

        # Wait for Keypress To Move To Next State
        key_pressed = False
        while not key_pressed:
            self.screen.blit(text, textRect)
            self.screen.blit(text0, textRect0)
            self.screen.blit(text1, textRect1)
            self.screen.blit(text2, textRect2)
            self.screen.blit(text3, textRect3)
            self.screen.blit(text4, textRect4)
            pg.display.update()

            for e in pg.event.get():
                if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.game.game_over()
                elif e.type == pg.KEYDOWN and e.key == pg.K_BACKSPACE:
                    key_pressed = True

        self.h = 0  # highscores is off
        self.game.menu()

    def increment_score(self): 
        self.score += self.settings.alien_points
        self.prep_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def reset(self): 
        self.score = 0
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)