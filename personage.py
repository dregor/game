from g_object import G_Object
from geometry import Geo
from math import sin, pi
from Box2D import b2Vec2 as Vec2
import Box2D as b2
from BitMasks import Bits

class Personage(G_Object):
    def add_part(self, body):
        trans = self.body.position - body.position
        for fixture in body.fixtures:
            fixture.filterData.maskBits = Bits.PERSONAGE_MASK
            fixture.filterData.categoryBits = Bits.PERSONAGE_BITS
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

    def __init__(self, game, position=(0, 0), angle=0, dynamic=True, additive=(0, 0), is_inside=True, is_you=False):
        G_Object.__init__(self, game, position, angle, dynamic, additive, is_inside)
        self.is_you = is_you
        self.parts = []
        self.add_part(self.body)

        if self.is_you:
            self.center_box = game.world.CreateDynamicBody(position=self.position,
                                                           shapes=b2.b2PolygonShape(box=(0.5, 0.5)))
            for item in self.center_box.fixtures:
                item.filterData.maskBits = Bits.NOTHING_MASK
                item.filterData.categoryBits = Bits.NOTHING_BITS

            game.world.CreatePrismaticJoint(bodyA=game.maw.center_box,
                                            bodyB=self.center_box,
                                            axis=(0, -1))

            game.world.CreateRevoluteJoint(bodyA=self.center_box,
                                           bodyB=self.body)
