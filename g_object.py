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
        self.body.userData = self

    def event(self, event):
        pass

    def draw(self):
        center = self.surface.current.get_rect().center
        pos = self.game.to_screen(self.position)
        self.game.screen.blit( self.surface.current , (pos[0]-center[0],pos[1]-center[1]))

    def update(self):
        self.surface.transform( self.body.angle, self.game.camera.zoom )

