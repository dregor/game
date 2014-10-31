import pygame


class G_Surface():
    def __init__(self, image=None):
        if image is None:
            self.origin = pygame.Surface((0, 0))
            self.origin.set_alpha(0)
        else:
            self.load(image)

        self.current = self.origin.copy()

    def load(self, image):
        self.origin = pygame.image.load(image).convert_alpha()

    def transform(self, angle, zoom=0):
        if self.origin.get_size() != (0, 0):
            self.current = _rotozoom(self.origin, angle, zoom).copy()


def _rotozoom(image, angle, zoom):
    from math import degrees

    angle = degrees(angle)
    if angle != 0:

        rot_image = pygame.transform.rotozoom(image, angle, zoom)
        rot_rect = rot_image.get_rect().copy()
        cx, cy = rot_image.get_rect().x, rot_image.get_rect().y
        rot_rect.x, rot_rect.y = cx * zoom, cy * zoom
        rot_image = rot_image.subsurface(rot_rect).copy()

        return rot_image
    else:
        return image
