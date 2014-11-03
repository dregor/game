import random

from g_object import g_object


class Bactery(g_object):
    images = ['images/ameb.gif', 'images/bakt.gif', 'images/microb.gif']

    def __init__(self, game, position=(0, 0), angle=0, name=''):
        g_object.__init__(self, game, position, angle)
        self.surface.load(random.sample(self.images, 1)[0])
        size = self.surface.origin.get_size()
        self.name = name
        self.radius = ((size[0] + size[1]) / 4) / game.PPM
        self.body.CreateCircleFixture(radius=self.radius, density=50, friction=1.3)
        self.additive = (0, self.radius)

    def draw(self):
        g_object.draw(self)
        self.game.debuger.text_out(self.name, self.game.to_screen(self.position))

    def update(self):
        g_object.update(self)
