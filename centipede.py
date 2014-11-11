import random
import pygame
from pygame.locals import *
from personage import Personage
import Box2D as b2
from math import pi
from Box2D import b2Vec2 as Vec2


class Centipede(Personage):
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, name='', speed=8000, is_you=False, is_inside=True):
        Personage.__init__(self, game, position, angle, name=name, speed=speed, is_you=is_you, is_inside=is_inside)

    def event(self, event):
        Personage.event(self, event)

    def move(self, direction=1):
        pass

    def draw(self):
        Personage.draw(self)

    def update(self):
        if not self.is_you:
            pass
        Personage.update(self)
        if self.MOVE_LEFT:
            self.move(-1)
        if self.MOVE_RIGHT:
            self.move()