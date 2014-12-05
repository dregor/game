from math import pi
from Box2D import b2Vec2 as Vec2
from bits_masks import Bits
from gameobject import GameObject
import Box2D as B2
from geometry import Geo
import pygame


class Composite():
    def give_all_obj(self):
        for item in self.parts:
            if isinstance(item['obj'], GameObject):
                yield item['obj']
            elif isinstance(item['obj'], Composite):
                for i in item['obj'].give_all_obj():
                    yield i

    def get_position(self):
        return self.body.body.position

    def set_position(self, val):
        for obj in self.parts:
            obj['obj'].set_position((val[0] + obj['trans'][0], val[1] + obj['trans'][1]))

    def get_angle(self):
        return self.body.body.angle

    def set_angle(self, val):
        for b in self.parts:
            b['trans'] = Geo.to_angle((0, 0), b['trans'], val)
            b['obj'].set_position(Vec2(b['trans']) + self.get_position())
            b['obj'].set_angle(val)

    @property
    def is_inside(self):
        return self._is_inside

    @is_inside.setter
    def is_inside(self, val):
        for b in self.give_all_obj():
            b.is_inside = val

    def mirror(self, orientation=(-1, 1)):
        for part in self.parts:
            part['obj'].mirror(orientation=orientation)
            part['trans'] = (part['trans'][0] * orientation[0], part['trans'][1] * orientation[1])
            part['obj'].set_position(
                (self.get_position()[0] + part['trans'][0], self.get_position()[1] + part['trans'][1]))
            '''
            q = Geo.quarter(self.get_position(), part['obj'].get_position())
            if q == 2 or 4:
            '''
            part['obj'].set_angle(part['obj'].get_angle() * -2)

        for joint in self.joints:
            if joint.type == 1:
                new_joint = B2.b2RevoluteJointDef()
                # new_joint.enableLimit = joint.limitEnabled
                #new_joint.lowerAngle = joint.lowerLimit - pi
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
            anchor_a = Geo.to_angle(joint.bodyA.position, joint.anchorA, joint.bodyA.angle)
            new_joint.localAnchorA = (anchor_a[0] * orientation[0], anchor_a[1] * orientation[1])
            anchor_b = Geo.to_angle(joint.bodyB.position, joint.anchorB, joint.bodyB.angle)
            new_joint.localAnchorB = (anchor_b[0] * orientation[0], anchor_b[1] * orientation[1])
            new_joint.collideConnected = joint.collideConnected
            self.game.world.DestroyJoint(joint)
            self.game.world.CreateJoint(new_joint)

    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, name='', body=None):
        self.name = name
        self._is_inside = is_inside
        self.game = game
        self.parts = []
        self.joints = []
        self.old_angle = angle
        if body:
            self.body = body
        else:
            self.body = self.game.world.CreateDynamicBody(
                position=position,
                shapes=B2.b2PolygonShape(box=(0.5, 0.5)))
            for item in self.body.fixtures:
                item.filterData.maskBits = Bits.NOTHING_MASK
                item.filterData.categoryBits = Bits.NOTHING_BITS
        self.add_part(self.body)

    def add_part(self, obj):
        trans = Vec2(obj.get_position() - self.get_position())
        if isinstance(obj, GameObject):
            for fixture in obj.body.fixtures:
                fixture.filterData.maskBits = Bits.PARTS_MASK
                fixture.filterData.categoryBits = Bits.PARTS_BITS
        self.parts.append({'obj': obj, 'trans': trans})

    def event(self, event):
        for item in self.parts:
            item['obj'].event(event)

    def update(self):
        change_angle = self.get_angle() - self.old_angle
        for item in self.parts:
            if change_angle != 0:
                item['trans'] = Geo.to_angle((0, 0), item['trans'], -1 * change_angle)

            item['obj'].update()
        self.old_angle = self.get_angle()

    def draw(self):
        for item in self.parts:
            # item['obj'].draw()
            pt = Vec2(item['trans']) + self.get_position()
            pygame.draw.circle(self.game.screen, (20, 0, 0), self.game.to_screen(pt),
                               int(3 * self.game.camera.zoom), 1)

        '''
        self.game.debuger.text_out('_' * 4 + '{0:.2f} : {1:.2f}'.format(self.get_position().x, self.get_position().y),
                                    Vec2(self.game.to_screen(self.get_position())))
        self.game.debuger.text_out('_' * 4 + '{0} - {1}'.format(self.__class__.__name__, self.name),
                                    Vec2(self.game.to_screen(self.get_position())) + Vec2(0, 10))
        self.game.debuger.text_out('_' * 4 + '{0:f}'.format(degrees(self.get_angle())),
                                    Vec2(self.game.to_screen(self.get_position())) + Vec2(0, 24))
        for i in range(0, len(self.joints)):
            self.game.debuger.text_out(
                '_' * 4 + '{0:.2f} : {1:.2f}'.format(self.joints[i].anchorA[0], self.joints[i].anchorA[1]),
                Vec2(self.game.to_screen(self.get_position())) + Vec2(0, 23 + (i + 1) * 12))
        '''