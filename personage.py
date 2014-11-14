from composite import Composite
import Box2D as b2
from bits_masks import Bits
from Box2D import b2Vec2 as Vec2
import pygame
from pygame.locals import *
from random import randint


class Personage(Composite):
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, additive=(0, 0), name='', speed=100, is_inside=True,
                 is_you=False, g_body=None):
        Composite.__init__(self, game=game, position=position, angle=angle, is_inside=is_inside)
        self.is_you = is_you
        self.name = name
        self.speed = speed
        self.g_body = g_body
        self.additive = additive
        self.add_part(g_body)

        for fixture in self.g_body.body.fixtures:
            fixture.filterData.maskBits = Bits.PERSONAGE_MASK
            fixture.filterData.categoryBits = Bits.PERSONAGE_BITS

        if self.is_you:
            self.center_box = self._game.world.CreateDynamicBody(position=self.position,
                                                                 shapes=b2.b2PolygonShape(box=(0.5, 0.5)))
            for item in self.center_box.fixtures:
                item.filterData.maskBits = Bits.NOTHING_MASK
                item.filterData.categoryBits = Bits.NOTHING_BITS

            self._game.world.CreatePrismaticJoint(bodyA=self._game.maw.center_box,
                                                  bodyB=self.center_box,
                                                  axis=(0, -1))

            self._game.world.CreateRevoluteJoint(bodyA=self.center_box,
                                                 bodyB=self.g_body.body)

    def move(self, direction=1):
        pass

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
        self._game.debuger.text_out('_' * 4 + '{0:.3f} : {1:.3f}'.format(self.position.x, self.position.y),
                                    self._game.to_screen(self.position))
        self._game.debuger.text_out('_' * 4 + '{0} - {1}'.format(self.__class__.__name__, self.name),
                                    Vec2(self._game.to_screen(self.position)) + Vec2(0, 10))

    def update(self):
        Composite.update(self)
        if not self.is_you:
            rand = randint(-1, 1)
            if rand != 0:
                self.move(rand * 0.5)
        if self.MOVE_LEFT:
            self.move(-1)
        if self.MOVE_RIGHT:
            self.move()