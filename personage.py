from composite import Composite
import Box2D as B2
from bits_masks import Bits
from Box2D import b2Vec2 as Vec2
import pygame
from pygame.locals import *
from random import randint
from math import degrees

class Personage(Composite):
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, additive=(0, 0), name='', speed=100, is_inside=True,
                 is_you=False, body=None, orientation=0):
        Composite.__init__(self, game=game, position=position, angle=angle, is_inside=is_inside, body=body)
        self.is_you = is_you
        self.name = name
        self.speed = speed
        self.additive = additive
        self.orientation = orientation

        for fixture in self.body.body.fixtures:
            fixture.filterData.maskBits = Bits.PERSONAGE_MASK
            fixture.filterData.categoryBits = Bits.PERSONAGE_BITS

        if self.is_you:
            self.center_box = self.game.world.CreateDynamicBody(position=self.get_position(),
                                                                shapes=B2.b2PolygonShape(box=(0.5, 0.5)))
            for item in self.center_box.fixtures:
                item.filterData.maskBits = Bits.NOTHING_MASK
                item.filterData.categoryBits = Bits.NOTHING_BITS

            self.game.world.CreatePrismaticJoint(bodyA=self.game.maw.center_box,
                                                 bodyB=self.center_box,
                                                 axis=(0, -1))

            self.game.world.CreateRevoluteJoint(bodyA=self.center_box,
                                                bodyB=self.body.body)

    def move(self, direction=1):
        if direction < 0:
            if not self.orientation:
                self.mirror()
                self.orientation = 1
        elif direction > 0:
            if self.orientation:
                self.mirror()
                self.orientation = 0

    def event(self, event):
        Composite.event(self, event)
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
        Composite.draw(self)

    def update(self):
        Composite.update(self)
        if not self.is_you:
            rand = randint(-3, 3)
            if rand != 0:
                self.move(rand)
        if self.MOVE_LEFT:
            self.move(-1)
        if self.MOVE_RIGHT:
            self.move()
