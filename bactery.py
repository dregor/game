import pygame
from Box2D.b2 import *
from g_object import G_Object

class Bactery(G_Object):
    image = 'images/microb.gif'

    def __init__(self, game, position = (0,0), angle=0):
        G_Object.__init__(self, game, position, angle)
        self.sprite = pygame.image.load(self.image).convert_alpha()
        self.body_circle = self.body.CreateCircleFixture(radius = 2, density=1, friction=0.3)

    def draw(self):
        self.game.screen.blit( self.sprite, ( self.body.position[0]*self.game.PPM - self.sprite.get_width()/2, (self.game.SCREEN_HEIGHT - self.position[1]) *self.game.PPM- self.sprite.get_height()/2) )

    def update(self):
        pass
