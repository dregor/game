import random
from personage import Personage
import Box2D as b2


class Bactery(Personage):
    def __init__(self, game, position=(0, 0), angle=0, name='', speed=300, is_inside=True, is_you=False):
        Personage.__init__(self, game=game, position=position, angle=angle, name=name, speed=speed, is_inside=is_inside,
                           is_you=is_you)
        size = self.surface.origin.get_size()
        self.radius = ((size[0] + size[1]) / 4) / game.PPM
        self.body.CreateCircleFixture(radius=self.radius,
                                      density=35,
                                      friction=1.8)

        self.additive = (0, self.radius)

        if self.is_you:
            self.center_box = game.world.CreateDynamicBody(position=self.position,
                                                           shapes=b2.b2PolygonShape(box=(0.5, 0.5)))

            game.world.CreatePrismaticJoint(bodyA=game.maw.center_box,
                                            bodyB=self.center_box,
                                            axis=(0, 1))

            game.world.CreateRevoluteJoint(bodyA=self.center_box,
                                           bodyB=self.body)

    def move(self, direction=1):
        self.body.ApplyAngularImpulse(self.speed * direction * self.radius, wake=True)

    def draw(self):
        Personage.draw(self)

    def update(self):
        Personage.update(self)