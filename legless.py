import random
import pygame
from pygame.locals import *
from personage import Personage
import Box2D as b2
from math import pi


class LegLess(Personage):
    images = ['images/ameb.gif', 'images/bakt.gif', 'images/microb.gif']
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, name='', speed=10000, is_you=False, is_inside=True,
                 angle_vector=(0, 1)):
        Personage.__init__(self, game, position, angle, is_inside=is_inside)
        self.speed = speed
        self.is_you = is_you
        self.surface.load(random.sample(self.images, 1)[0])
        size = self.surface.origin.get_size()
        self.name = name
        r = self.radius = ((size[0] + size[1]) / 4) / game.PPM
        self.additive = (0, self.radius)

        self.body.CreateCircleFixture(radius=self.radius,
                                      density=9,
                                      friction=8)

        cdb = game.world.CreateDynamicBody

        self.left_leg = cdb(position=self.position + b2.b2Vec2(-r, -r + 0.4), angle=angle)
        self.left_leg.CreatePolygonFixture(vertices=[(-r / 2, 0.4), (r / 2, 0.4), (r / 2, -0.4), (-r / 2, -0.4)],
                                           density=1.5,
                                           friction=8)
        self.left_leg.CreatePolygonFixture(vertices=[(-r / 2, -0.4), (-r / 4, -0.4), (-3 * r / 8, -0.8)],
                                           density=0.5,
                                           friction=8)
        self.add_part(self.left_leg)
        j1 = game.world.CreateRevoluteJoint(bodyA=self.left_leg,
                                            bodyB=self.body,
                                            localAnchorA=(r - 0.4, 0),
                                            localAnchorB=(0, 0.4 - r))
        j1.limitEnabled = True
        j1.upperLimit = pi / 8
        j1.lowerLimit = - pi / 8

        self.right_leg = cdb(position=self.position + b2.b2Vec2(r, r - 0.4), angle=angle)
        self.right_leg.CreatePolygonFixture(vertices=[(-r / 2, 0.4), (r / 2, 0.4), (r / 2, -0.4), (-r / 2, -0.4)],
                                            density=1.5,
                                            friction=8)
        self.right_leg.CreatePolygonFixture(vertices=[(r / 2, -0.4), (r / 4, -0.4), (3 * r / 8, -0.8)],
                                            density=0.5,
                                            friction=8)
        self.add_part(self.right_leg)
        j2 = game.world.CreateRevoluteJoint(bodyA=self.right_leg,
                                            bodyB=self.body,
                                            localAnchorA=(-r + 0.4, 0),
                                            localAnchorB=(0, -0.4 + r))

        j2.limitEnabled = True
        j2.upperLimit = pi / 8
        j2.lowerLimit = - pi / 8

        if self.is_you:
            self.center_box = game.world.CreateDynamicBody(position=self.position,
                                                           shapes=b2.b2PolygonShape(box=(0.5, 0.5)))
            for item in self.center_box.fixtures:
                item.filterData.maskBits = 0x0003
                item.filterData.categoryBits = 0x0000

            game.world.CreatePrismaticJoint(bodyA=game.maw.center_box,
                                            bodyB=self.center_box,
                                            axis=angle_vector)

            game.world.CreateRevoluteJoint(bodyA=self.center_box,
                                           bodyB=self.body)

    def event(self, event):
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

    def move(self, direction=1):
        self.body.ApplyTorque(self.speed * direction * self.radius, wake=True)

    def draw(self):
        Personage.draw(self)
        self.game.debuger.text_out(self.name + '  -  ' + str(self.position), self.game.to_screen(self.position))

    def update(self):
        Personage.update(self)
        if self.MOVE_LEFT:
            self.move(-1)
        if self.MOVE_RIGHT:
            self.move()
