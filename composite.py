from math import sin, pi
from Box2D import b2Vec2 as Vec2
from bits_masks import Bits
from gameobject import GameObject
import Box2D as B2
from geometry import Geo
import pygame


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
            part['obj'].mirror()
            part['trans'] = (part['trans'][0] * -1, part['trans'][1] * -1)
            part['obj'].set_position(self.get_position() + part['trans'])
            # part['obj'].set_angle(part['obj'].get_angle() - pi/2)
        for joint in self.joints:
            if joint.type == 1:
                new_joint = B2.b2RevoluteJointDef()
                # new_joint.enableLimit = joint.limitEnabled
                # new_joint.lowerAngle = joint.lowerLimit - pi
                #new_joint.upperAngle = joint.upperLimit - pi
            elif joint.type == 2:
                new_joint = B2.b2PrismaticJointDef
            elif joint.type == 3:
                new_joint = B2.b2DistanceJointDef
            elif joint.type == 4:
                new_joint = B2.b2PulleyJointDef
            elif joint.type == 7:
                new_joint = B2.b2WheelJointDef
            elif joint.type == 8:
                new_joint = B2.b2WeldJointDef
            elif joint.type == 9:
                new_joint = B2.b2FrictionJointDef
            elif joint.type == 10:
                new_joint = B2.b2RopeJointDef
            new_joint.bodyA = joint.bodyA
            new_joint.bodyB = joint.bodyB
            anchor_a = Geo.to_angle(joint.bodyA.position, joint.anchorA, - joint.bodyA.angle)
            anchor_a -= joint.bodyA.position
            new_joint.localAnchorA = (anchor_a[0] * -1, anchor_a[1] * -1)
            anchor_b = Geo.to_angle(joint.bodyB.position, joint.anchorB, - joint.bodyB.angle)
            anchor_b -= joint.bodyB.position
            new_joint.localAnchorB = (anchor_b[0] * -1, anchor_b[1] * -1)
            new_joint.collideConnected = joint.collideConnected
            self._game.world.DestroyJoint(joint)
            self._game.world.CreateJoint(new_joint)

    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, name=''):
        self._position = Vec2(position)
        self.name = name
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

            if isinstance(item['obj'], GameObject):
                new_angle = item['obj'].body.angle
            else:
                new_angle = item['obj']._parts[0]['obj'].body.angle

            old_angle = self.get_angle()

            if index == 0:
                self._position = item['obj'].body.position
                self._angle = new_angle

            #item['trans'] = Geo.to_angle(self.get_position(), item['trans'], old_angle - new_angle)

            item['obj'].update()


    def draw(self):
        for item in self._parts:
            item['obj'].draw()
            # self._game.debuger.DebugDraw.draw_circle_shape()  raw_point((254,254,254),)
            pygame.draw.circle(self._game.screen, (20, 20, 20), self._game.to_screen(Vec2(item['trans'])),
                               20 * self._game.camera.zoom, 1)