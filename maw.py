import pygame
from Box2D.b2 import *
import Box2D
from g_object import G_Object
#from g_surface import G_Surface

class Maw(G_Object):
    image = 'images/microb.gif'

    def __init__(self, game, position = (0,0), angle=0, radius = 10, n = 3 ):
        G_Object.__init__(self, game, position, angle)
 
        outside = self.polyhedron( (0,0), radius, n )
        #inside = self.polyhedron( position, radius + 1, n )
        vertices = outside
        fixture=Box2D.b2FixtureDef(
                shape=Box2D.b2PolygonShape(vertices=vertices), 
                density=1,
                friction=0.6,
                )
        self.body.CreateFixture(fixture)

        
    def polyhedron(self, pos = (0, 0), r = 1, n = 5):
        from math import cos, sin, pi
        vertices = []
        for i in range(n,0,-1):
            vertices.append( (int(pos[0] + (r *sin(2*i*pi/n))),int(pos[1] + (r * cos(2*i*pi/n)))) )
        return vertices  

    def draw(self):
        G_Object.draw(self)
        
    def update(self):
        G_Object.update(self)

