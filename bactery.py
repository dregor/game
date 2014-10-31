import random

from g_object import g_object


class Bactery(g_object):
    images = ['images/ameb.gif', 'images/bakt.gif', 'images/microb.gif']

    def __init__(self, game, position=(0, 0), angle=0):
        g_object.__init__(self, game, position, angle)
        self.surface.load(random.sample(self.images, 1)[0])
        size = self.surface.origin.get_size()
        radius = ((size[0] + size[1]) / 4) / game.PPM
        self.body.CreateCircleFixture(radius=radius, density=50, friction=2.3)
        self.additive = (0, radius)

    def draw(self):
        g_object.draw(self)

    def update(self):
        g_object.update(self)
