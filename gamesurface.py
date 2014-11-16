import pygame
from copy import copy


class GameSurface():
    def __init__(self, image=None):
        if image is None:
            self.origin = pygame.Surface((0, 0))
            self.origin.set_alpha(0)
        else:
            self.load(image)

        self.current = copy(self.origin.copy())

    def load(self, image):
        self.origin = pygame.image.load(image).convert_alpha()

    def transform(self, angle, zoom=0):
        if self.origin.get_size() != (0, 0):
            self.current = copy(_rotozoom(self.origin, angle, zoom))


def _rotozoom(image, angle, zoom):
    from math import degrees

    angle = degrees(angle)
    if angle != 0:

        rot_image = pygame.transform.rotozoom(image, angle, zoom)
        rot_rect = copy(rot_image.get_rect())
        cx, cy = rot_image.get_rect().x, rot_image.get_rect().y
        rot_rect.x, rot_rect.y = cx * zoom, cy * zoom
        rot_image = copy(rot_image.subsurface(rot_rect))

        return rot_image
    else:
        return image
