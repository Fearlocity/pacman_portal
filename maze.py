import pygame as pg
from pygame.sprite import Sprite, Group

class Node(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen

        self.image = pg.image.load('images/node.png')
        self.rect = self.image.get_rect()

        self.rect.left = self.rect.width
        self.rect.right = self.rect.height
        self.x = float(self.rect.x)

    def width(self):
        return self.rect.width
    
    def height(self):
        return self.rect.height
    
    def check_edges(self):
        return self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0
    
    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.draw()

class Grid:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.scoreboard = self.game.scoreboard
        self.nodes = Group()
        self.powerNodes = Group()

    def create_node(self, col, row):
        self.node = Node(game=self.game)
        self.rect = self.node.rect
        self.width, self.height = self.rect.size
        self.node.x = self.width + 2 * col * (self.width / 4 )
        self.rect.x = self.node.x
        self.rect.y = self.rect.height + 2 * col * (self.height / 4) * row
        self.nodes.add(self.node)

    def create_powerNode(self, col, row):
        self.powerNode = Node(game=self.game)
        self.powerNode.image = pg.image.load('images/powerNode.png')
        self.rect = self.powerNode.rect
        self.width, self.height = self.rect.size
        self.powerNode.x = self.width + 2 * col * (self.width / 4 )
        self.rect.x = self.powerNode.x
        self.rect.y = self.rect.height + 2 * col * (self.height / 4) * row
        self.powerNodes.add(self.powerNode)
    
    def check_collisions(self):
        
        if pg.sprite.spritecollide(self.game.player, self.nodes, True):
            if self.game.mainClock.get_time() % 2 == 0:
                self.game.sounds.play(0)
            print('Player got a Node')
            self.scoreboard.score += 10
        
        if pg.sprite.spritecollide(self.game.player, self.powerNodes, True):
            self.settings.bluemode = 1
            self.game.blinky.startF, self.game.blinky.endF = 0, 1
            self.game.pinky.startF, self.game.pinky.endF = 0, 1
            self.game.inky.startF, self.game.inky.endF = 0, 1
            self.game.clyde.startF, self.game.clyde.endF = 0, 1
            self.game.blinky.currentFrame, self.game.pinky.currentFrame, self.game.inky.currentFrame, self.game.clyde.currentFrame = 0, 0, 0, 0
            self.game.scoreboard.score += 50
            print('Time to Eat Ghost')

        if len(self.nodes) == 0:
            self.game.scoreboard.level += 1
            self.game.settings.enemySpeed += 1
            self.reset_grid()
            print('No More Nodes!!! RESET')

    def reset_grid(self):
        for row in range(14, 200, 3):
            for col in range(6, 100, 3):
                self.create_node(col, row)
        
        self.create_powerNode(col=5, row=19)
        self.create_powerNode(col=98, row=19)
        self.create_powerNode(col=5, row=94)
        self.create_powerNode(col=98, row=94)

    def update(self):
        self.check_collisions()
        for node in self.nodes.sprites():
            node.update()
        for powerNode in self.powerNodes.sprites():
            powerNode.update()