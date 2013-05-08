import pygame
from pygame.locals import *

class Bactery():
    image = 'images/microb.gif'
    _position = (0,0)

    @property
    def position( self ):
        return self._position
    @position.setter
    def position(self, val):
        self._position = val

    def __init__(self, game):
        self.game = game
        self.sprite = pygame.image.load(self.image).convert_alpha()


    def draw(self):
        self.game.screen.blit( self.sprite, ( self.position ) )

    def update(self):
       x, y = pygame.mouse.get_pos()
       if self.position[0] < x: self.position = ( self.position[0] + 1,self.position[1] )
       if self.position[0] > x: self.position = ( self.position[0] - 1,self.position[1] )
       if self.position[0] < y: self.position = ( self.position[0],self.position[1] + 1 )
       if self.position[0] > y: self.position = ( self.position[0],self.position[1] - 1 )
