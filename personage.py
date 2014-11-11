from g_object import G_Object
from geometry import Geo
from math import sin, pi
from Box2D import b2Vec2 as Vec2
import Box2D as b2
from BitMasks import Bits
import pygame
from pygame.locals import *
from random import sample, randint


class Personage(G_Object):
    images = ['images/ameb.gif', 'images/bakt.gif', 'images/microb.gif']
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def add_part(self, body):
        trans = self.body.position - body.position
        if body is not self.body:
            for fixture in body.fixtures:
                fixture.filterData.maskBits = Bits.PARTS_MASK
                fixture.filterData.categoryBits = Bits.PARTS_BITS
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

    def __init__(self, game, position=(0, 0), angle=0, additive=(0, 0), name='', speed=100, is_inside=True,
                 is_you=False):
        G_Object.__init__(self, game=game, position=position, angle=angle, dynamic=True, additive=additive,
                          is_inside=is_inside)
        self.surface.load(sample(self.images, 1)[0])
        self.is_you = is_you
        self.name = name
        self.speed = speed
        self.parts = []
        self.add_part(self.body)
        for fixture in self.body.fixtures:
            fixture.filterData.maskBits = Bits.PERSONAGE_MASK
            fixture.filterData.categoryBits = Bits.PERSONAGE_BITS

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

    def move(self, direction=1):
        pass

    def event(self, event):
        G_Object.event(self, event)
        if self.is_you:
            if event.type == KEYDOWN:
                key = pygame.key.get_pressed()

                if key[K_LEFT]:
                    self.MOVE_LEFT = True

                if key[K_RIGHT]:
                    self.MOVE_RIGHT = True

                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.MOVE_LEFT = False
                    if event.key == K_RIGHT:
                        self.MOVE_RIGHT = False

    def draw(self):
        G_Object.draw(self)
        self.game.debuger.text_out(self.name + '  -  ' + str(self.position), self.game.to_screen(self.position))

    def update(self):
        G_Object.update(self)
        if not self.is_you:
            rand = randint(-3, 3)
            if rand != 0:
                self.move(rand)
        if self.MOVE_LEFT:
            self.move(-1)
        if self.MOVE_RIGHT:
            self.move()