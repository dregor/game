from pygame.locals import *
import pygame


class Camera():
    zoom = 1.
    zoom_level = 0
    UP = False
    DOWN = False
    LEFT = False
    RIGHT = False
    Z_PLUS = False
    Z_MINUS = False

    def update(self):
        if self.UP:
            self.offset = (self.offset[0], self.offset[1] + 8)
        if self.DOWN:
            self.offset = (self.offset[0], self.offset[1] - 8)
        if self.RIGHT:
            self.offset = (self.offset[0] + 8, self.offset[1])
        if self.LEFT:
            self.offset = (self.offset[0] - 8, self.offset[1])
        if self.Z_PLUS:
            self.set_zoom(self.zoom_level - 0.08)
        if self.Z_MINUS:
            self.set_zoom(self.zoom_level + 0.04)

    def event(self, event):
        if event.type == KEYDOWN:
            key = pygame.key.get_pressed()
            if key[K_w]:
                self.UP = True

            if key[K_s]:
                self.DOWN = True

            if key[K_a]:
                self.LEFT = True

            if key[K_d]:
                self.RIGHT = True

            if key[K_q]:
                self.Z_MINUS = True

            if key[K_e]:
                self.Z_PLUS = True

        if event.type == KEYUP:
            if event.key == K_w:
                self.UP = False

            if event.key == K_s:
                self.DOWN = False

            if event.key == K_a:
                self.LEFT = False

            if event.key == K_d:
                self.RIGHT = False

            if event.key == K_q:
                self.Z_MINUS = False

            if event.key == K_e:
                self.Z_PLUS = False


    def set_zoom(self, val):
        if val == 0:
            self.zoom = 1.
        elif val < 0:
            self.zoom = 1 / (-1. * val + 1)
        else:
            self.zoom = val + 1
        self.zoom_level = val

    def __init__(self, game, offset=(0, 0), angle=0, zoom_level=0):
        self.game = game
        self.offset = offset
        self.angle = angle
        self.set_zoom(zoom_level)

