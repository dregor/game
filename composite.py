from geometry import Geo
from math import sin, pi
from Box2D import b2Vec2 as Vec2
from bits_masks import Bits
from g_object import G_Object


class Composite():

    def give_all_obj(self):
        for item in self._parts:
            if isinstance(item['obj'], G_Object):
                yield item['obj']
            elif isinstance(item['obj'], Composite):
                for i in item['obj'].give_all_obj():
                    yield i

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        for obj in self._parts:
            obj['obj'].position = Vec2(val) + Vec2(obj['trans'])

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        for b in self._parts:
            b['trans'] = (Geo.length(self.position, b['trans']) * sin(Geo.alpha(self.position, b['trans'])) - val,
                          Geo.length(self.position, b['trans']) *
                          sin(pi / 2 - Geo.alpha(self.position, b['trans'])) + val)
            b['obj'].position += b['trans']
            b['obj'].angle = val

    @property
    def is_inside(self):
        return self._is_inside

    @is_inside.setter
    def is_inside(self, val):
        for b in self.give_all_obj():
            b.is_inside = val

    def __init__(self, game, position=(0, 0), angle=0, is_inside=True):
        self._position = Vec2(position)
        self._angle = angle
        self._is_inside = is_inside
        self._game = game
        self._parts = []

    def add_part(self, obj):
        trans = self.position - obj.position
        if isinstance(obj, G_Object):
            for fixture in obj.body.fixtures:
                fixture.filterData.maskBits = Bits.PARTS_MASK
                fixture.filterData.categoryBits = Bits.PARTS_BITS
        self._parts.append({'obj': obj, 'trans': trans})

    def event(self, event):
        for item in self.give_all_obj():
            item.event(event)

    def update(self):
        for item in self.give_all_obj():
            item.update()

    def draw(self):
        for item in self.give_all_obj():
            item.draw()