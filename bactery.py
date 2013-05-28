from Box2D.b2 import *
from g_object import G_Object
import random
import Box2D

class Bactery(G_Object):
    images = ['images/ameb.gif','images/bakt.gif','images/microb.gif']

    def __init__(self, game, position = (0,0), angle=0):
        G_Object.__init__(self, game, position, angle)
        self.surface.load(random.sample(self.images,1)[0])
        radius = ((self.surface.origin.get_size()[0]+self.surface.origin.get_size()[1])/4)/game.PPM
        self.body.CreateCircleFixture(radius = radius, density=50, friction=2.3)
        #self.body.CreateFixture(shape = Box2D.b2PolygonShape(vertices=[(0,3),(-1,-1),(1,-1)]), density = 10, friction = 1)
        self.additive = (0,radius)


    def draw(self):
        G_Object.draw(self)

    def update(self):
        G_Object.update(self)
