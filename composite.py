from geometry import Geo
from math import sin, pi
from Box2D import b2Vec2 as Vec2
from bits_masks import Bits
from gameobject import GameObject
import Box2D as B2


class Composite():

    def give_all_obj(self):
        for item in self._parts:
            if isinstance(item['obj'], GameObject):
                yield item['obj']
            elif isinstance(item['obj'], Composite):
                for i in item['obj'].give_all_obj():
                    yield i

    def get_position(self):
        return Vec2(self._position)


    def set_position(self, val):
        for obj in self._parts:
            obj['obj'].set_position(Vec2(val) + Vec2(obj['trans']))
        self._position = val

    def get_angle(self):
        return self._angle

    def set_angle(self, val):
        for b in self._parts:
            b['trans'] = (
            Geo.length(self.get_position(), b['trans']) * sin(Geo.alpha(self.get_position(), b['trans'])) - val,
            Geo.length(self.get_position(), b['trans']) * sin(
                pi / 2 - Geo.alpha(self.get_position(), b['trans'])) + val)
            b['obj'].set_position(b['trans'])
            b['obj'].set_angle(val)

    @property
    def is_inside(self):
        return self._is_inside

    @is_inside.setter
    def is_inside(self, val):
        for b in self.give_all_obj():
            b.is_inside = val

    def mirror(self):
        for part in self._parts:
            part['obj'].mirror
            part['trans'] *= -1
            part['obj'].set_position(self.get_position() - part['trans'])
        for joint in self.joints:
            print(joint.type)

            # joint.anchorA = Vec2(0,0)
            # joint.anchorB *= (-1,-1)



    def __init__(self, game, position=(0, 0), angle=0, is_inside=True):
        self._position = Vec2(position)
        self._angle = angle
        self._is_inside = is_inside
        self._game = game
        self._parts = []
        self.joints = []

    def add_part(self, obj):
        trans = Vec2(self.get_position() - obj.get_position())
        if isinstance(obj, GameObject):
            for fixture in obj.body.fixtures:
                fixture.filterData.maskBits = Bits.PARTS_MASK
                fixture.filterData.categoryBits = Bits.PARTS_BITS
        self._parts.append({'obj': obj, 'trans': trans})

    def event(self, event):
        for item in self._parts:
            item['obj'].event(event)

    def update(self):
        for index, item in enumerate(self._parts):
            if index == 0:
                self._position = item['obj'].body.position - item['trans']
                self._angle = item['obj'].body.angle
            item['obj'].update()

    def draw(self):
        for item in self._parts:
            item['obj'].draw()