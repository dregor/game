import pygame
from pygame.locals import *
from pygame.color import *

class Debuger():
    _position = (0,0)

    @property
    def position( self ):
        return self._position
    @position.setter
    def position(self, val):
        self._position = val

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial',12)

    def draw(self):
        x, y = pygame.mouse.get_pos()
        self.game.screen.blit( self.game.font.render('fps : ' + str(self.game.clock.get_fps()), 1, THECOLORS['red']), self.position )
        self.game.screen.blit( self.game.font.render('mouse : ' + str(x) + ',' + str(y), 1, THECOLORS['red']), (self.position[0],self.position[1]+14) )

    def update(self):
        pass
