from Box2D.b2 import *
import Box2D
import pygame
from g_surface import G_Surface
class G_Object():

    @property
    def position( self ):
        return self.body.position

    @position.setter
    def position(self, val):
        self.body.position = val

    def image_position(self):
        position = self.game.to_screen(self.position)
        return ( position[0] - self.surface.origin.get_width()/2, position[1] - self.surface.origin.get_height()/2)

    def transform(self):
        pass

    def __init__(self, game, position = (0,0), angle=0, dynamic = True, additive=(0,0) ):
        self.game = game
        self.additive = additive

        if dynamic:
            bodyDef = self.game.world.CreateDynamicBody
        else:
            bodyDef = self.game.world.CreateStaticbody

        self.body = bodyDef(position = position, angle=angle)

        self.surface = G_Surface()
        self.body.angularDamping=.5

    def event(self, event):
        pass

    def draw(self):
        self.game.screen.blit( self.surface.current , self.image_position() )

    def update(self):
        self.surface.transform( self.body.angle, 0 )
