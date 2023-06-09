import pygame as pg
import time

class Sound:
    def __init__(self, sounds, playing):
        self.bg_music = 'sounds/start.mp3'
        self.sounds = {}
        self.playing = playing
        for sound in sounds:
            for k, v in sound.items():
                self.sounds[k] = pg.mixer.Sound(v)


    def play(self, sound):
        if self.playing and sound in self.sounds.keys():
            self.sounds[sound].play()

    def toggle(self):
        self.playing = not self.playing
        pg.mixer.music.play(-1, 0.0) if self.playing else pg.mixer.music.stop()

    def gameover(self):
        self.playing = False
        pg.mixer.music.stop()
        self.play('sounds/game_over.ogg')

    def pacmanDeath(self):
        pg.mixer.music.load('sounds/game_over.ogg')
        pg.mixer.music.play(1, 0.0)
        while pg.mixer.music.get_busy():
            time.sleep(0.02)

    def pacmanIntro(self):
        pg.mixer.music.load('sounds/start.mp3')
        pg.mixer.music.play(1, 0.0)
        while pg.mixer.music.get_busy():
            time.sleep(0.02)