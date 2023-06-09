class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 550
        self.screen_height = 700
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.bg_color = self.BLACK
        self.WALL_COLOR = (255, 0, 0)
        self.FPS = 60
        
        self.enemySpeed = 6
        self.pacmanSpeed = 6
        self.portalSpeed = 30

        self.lives = 3
        self.deaths = 0

        self.bluemode = 0
        self.m = 0
        self.h = 0 
        self.gameOver = 0


