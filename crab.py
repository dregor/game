from g_object import g_object


class Crab(g_object):
    def __init__(self, game, position=(0, 0), angle=0):
        g_object.__init__(self, game, position, angle)

    def draw(self):
        g_object.draw(self)

    def update(self):
        g_object.update(self)
