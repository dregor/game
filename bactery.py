import random
import pygame
from pygame.locals import *
from g_object import g_object


class Bactery(g_object):
    images = ['images/ameb.gif', 'images/bakt.gif', 'images/microb.gif']
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, name='', speed=50, is_you=False):
        g_object.__init__(self, game, position, angle)
        self.speed = speed
        self.is_you = is_you
        self.surface.load(random.sample(self.images, 1)[0])
        size = self.surface.origin.get_size()
        self.name = name
        self.radius = ((size[0] + size[1]) / 4) / game.PPM
        self.body.CreateCircleFixture(radius=self.radius, density=17, friction=8)
        self.additive = (0, self.radius)

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
        g_object.draw(self)
        self.game.debuger.text_out(self.name, self.game.to_screen(self.position))

    def update(self):
        g_object.update(self)
        if self.MOVE_LEFT:
            self.move()
        if self.MOVE_RIGHT:
            self.move(-1)
