import pygame
from Box2D.b2 import *
import Box2D
from g_object import G_Object

class Maw(G_Object):
    inside_obj = []
    outside_obj = []

    def __init__(self, game, position = (0,0), angle=0, radius = 10, n = 3 ):
        G_Object.__init__(self, game, position, angle)
        for vertices in self.polyhedron( r = radius, n = n ):
            fixture=Box2D.b2FixtureDef(
                    shape=Box2D.b2PolygonShape(vertices=vertices),
                    density=1,
                    friction=0.6,
                    )
            self.body.CreateFixture(fixture)
        self.center = self.game.world.CreateStaticBody(
                                                    position=position,
                                                    shapes = polygonShape(box=(1,1))
                                                )

        joint = self.game.world.CreateRevoluteJoint(bodyA=self.body,bodyB=self.center,anchor = self.body.worldCenter )


    def _polyhedron(self, r , n ):
        from math import cos, sin, pi
        vertices = []
        for i in range(n,0,-1):
            vertices.append(( r *sin(2*i*pi/n),r * cos(2*i*pi/n) ))
        return vertices

    def polyhedron(self, r =1, n= 5):
        outside = self._polyhedron( r + 2, n )
        outside.append(outside[0])
        inside = self._polyhedron( r, n )
        inside.append(inside[0])
        for i in range(n):
            yield [ outside[i], outside[i+1], inside[i], inside[i+1] ]

    def draw(self):
        G_Object.draw(self)

    def update(self):
        G_Object.update(self)

