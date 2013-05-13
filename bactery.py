import pygame
import Box2D
from Box2D.b2 import *
from g_object import G_Object

class Bactery(G_Object):
    image = 'images/microb.gif'

    def __init__(self, game, position = (0,0), angle=0):
        super(G_Object,self).__init__()
        self.sprite = pygame.image.load(self.image).convert_alpha()
        self.body_circle = self.body.CreateCircleFixture(radius = 2, density=1, friction=0.3)

    def draw_circle(self):
        position=self.body.transform*self.body_circle.shape.pos*self.game.PPM
        position=(position[0], self.game.SCREEN_HEIGHT-position[1])
        pygame.draw.circle(self.game.screen, (30,150,40), [int(x) for x in position], int(self.body_circle.shape.radius*self.game.PPM))

    def draw(self):
        self.game.screen.blit( self.sprite, ( self.position[0] - self.sprite.get_width()/2, self.position[1]- self.sprite.get_height()/2) )
        if self.game.debug:
            self.draw_circle()

    def update(self):
        pos = self.body.position*self.game.PPM
        self.position = (pos[0],self.game.SCREEN_HEIGHT - pos[1] )
