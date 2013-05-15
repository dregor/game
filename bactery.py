import pygame
from Box2D.b2 import *
from g_object import G_Object

class Bactery(G_Object):
    image = 'images/microb.gif'

    def __init__(self, game, position = (0,0), angle=0):
        G_Object.__init__(self, game, position, angle)
        self.sprite = pygame.image.load(self.image).convert_alpha()
        self.body_circle = self.body.CreateCircleFixture(radius = 2, density=1, friction=1.3)

    def pos(self):
        return ( self.position[0]*self.game.PPM - self.sprite.get_width()/2, self.game.HEIGHT - self.position[1] *self.game.PPM- self.sprite.get_height()/2)

    def draw(self):
        self.game.screen.blit( self.sprite, self.pos() )

    def rot_center(self,image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):
        self.sprite = self.rot_center(self.sprite,self.body.angle)

