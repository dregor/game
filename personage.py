from g_object import G_Object
from geometry import Geo
from math import sin, pi
from Box2D import b2Vec2 as Vec2
import Box2D as b2


class Personage(G_Object):
    def add_part(self, body):
        trans = self.body.position - body.position
        self.parts.append({'body': body, 'trans': trans})

    @property
    def position(self):
        return self.body.position

    def set_position(self, val):
        for b in self.parts:
            b['body'].position = Vec2(val) + Vec2(b['trans'])

    @property
    def angle(self):
        return self.body.angle

    def set_angle(self, val):
        for b in self.parts:
            b['trans'] = (Geo.length(self.position, b['trans']) * sin(Geo.alpha(self.position, b['trans'])) - val,
                          Geo.length(self.position, b['trans']) * sin(
                              pi / 2 - Geo.alpha(self.position, b['trans'])) + val)
            b['body'].position += b['trans']
            b['body'].angle = val

    def __init__(self, game, position=(0, 0), angle=0, dynamic=True, additive=(0, 0), is_inside=True):
        G_Object.__init__(self, game, position, angle, dynamic, additive, is_inside)
        self.parts = []
        self.add_part(self.body)
