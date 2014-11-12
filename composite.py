from geometry import Geo
from math import sin, pi
from Box2D import b2Vec2 as Vec2
from bits_masks import Bits
from g_object import G_Object


class Composite(G_Object):
    parts = []

    def give_all_obj(self):
        yield self
        for item in self.parts:
            if isinstance(item['obj'], G_Object):
                yield item['obj']
            elif isinstance(item['obj'], Composite):
                for i in item.give_all_obj():
                    yield i['obj']
            else:
                yield None

    @property
    def position(self):
        return self.body.position

    def set_position(self, val):
        for b in self.parts:
            b['obj'].position = Vec2(val) + Vec2(b['trans'])

    @property
    def angle(self):
        return self.body.angle

    def set_angle(self, val):
        for b in self.parts:
            b['trans'] = (Geo.length(self.position, b['trans']) * sin(Geo.alpha(self.position, b['trans'])) - val,
                          Geo.length(self.position, b['trans']) * sin(
                              pi / 2 - Geo.alpha(self.position, b['trans'])) + val)
            b['obj'].set_position += b['trans']
            b['obj'].set_angle = val

    def __init__(self, game, position=(0, 0), angle=0, additive=(0, 0), is_inside=True, image='images/default.png'):
        G_Object.__init__(self, game=game, position=position, angle=angle, dynamic=True, additive=additive,
                          is_inside=is_inside, image=image)
        self.add_part(self)

    def add_part(self, obj):
        trans = self.body.position - obj.body.position
        if (type(obj) == G_Object) or (obj is self):
            for fixture in obj.body.fixtures:
                fixture.filterData.maskBits = Bits.PARTS_MASK
                fixture.filterData.categoryBits = Bits.PARTS_BITS
        self.parts.append({'obj': obj, 'trans': trans})

    def event(self, event):
        G_Object.event(self, event)
        for item in self.give_all_obj():
            if item is G_Object:
                item.event(event)

    def update(self):
        G_Object.update(self)
        for item in self.give_all_obj():
            if item is G_Object:
                item.update()

    def draw(self):
        G_Object.draw(self)
        for item in self.give_all_obj():
            if item is G_Object:
                item.draw()