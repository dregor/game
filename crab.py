from g_object import Personage


class Crab(Personage):
    def __init__(self, game, position=(0, 0), angle=0):
        Personage.__init__(self, game, position, angle)

    def draw(self):
        Personage.draw(self)

    def update(self):
        Personage.update(self)
