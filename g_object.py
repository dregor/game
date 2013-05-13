import pygame
import Box2D
from Box2D.b2 import *

class G_Object():
    @property
    def position( self ):
        return self.body.position

    @position.setter
    def position(self, val):
        self.body.position = val

    def __init__(self, game, position = (0,0),angle=0 ):
        self.game = game
        self.body = self.game.world.CreateDynamicBody(position = position, angle=angle)

    def draw(self):
        pass

    def update(self):
        pass
