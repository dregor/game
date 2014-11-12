from composite import Composite
import Box2D as b2
from bits_masks import Bits
import pygame
from pygame.locals import *
from random import sample, randint


class Personage(Composite):
    images = ['images/ameb.gif', 'images/bakt.gif', 'images/microb.gif']
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, additive=(0, 0), name='', speed=100, is_inside=True,
                 is_you=False):
        Composite.__init__(self, game=game, position=position, angle=angle, additive=additive, is_inside=is_inside,
                           image=sample(self.images, 1)[0])
        self.is_you = is_you
        self.name = name
        self.speed = speed
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
        self.game.debuger.text_out(self.name + '  -  ' + str(self.position), self.game.to_screen(self.position))

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