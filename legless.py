from personage import Personage
import Box2D as b2
from math import pi
from Box2D import b2Vec2 as Vec2


class LegLess(Personage):
    def __init__(self, game, position=(0, 0), angle=0, name='', speed=8000, is_you=False, is_inside=True):
        Personage.__init__(self, game=game, position=position, angle=angle, name=name, speed=speed, is_you=is_you,
                           is_inside=is_inside)
        size = self.surface.origin.get_size()
        r = self.radius = ((size[0] + size[1]) / 4) / game.PPM
        self.additive = (0, self.radius)

        self.body.CreateCircleFixture(radius=self.radius,
                                      density=9,
                                      friction=8)

        cdb = game.world.CreateDynamicBody
        self.left_shoulder = cdb(position=self.position + Vec2(0, 0.4 - r),
                                 shapes=b2.b2PolygonShape(box=(0.4, 0.4)))

        game.world.CreateRevoluteJoint(bodyA=self.left_shoulder,
                                       bodyB=self.body,
                                       localAnchorA=(0, 0),
                                       localAnchorB=(0, 0.4 - r),
                                       collideConnected=False)

        self.add_part(self.left_shoulder)

        self.left_leg = cdb(position=self.position + Vec2(-r, -r + 0.4), angle=angle)
        self.left_leg.CreatePolygonFixture(
            vertices=[(-r / 1.5, 0.4), (r / 1.5, 0.4), (r / 1.5, -0.4), (-r / 1.5, -0.4)],
                                           density=1.5,
                                           friction=8)
        self.left_leg.CreatePolygonFixture(vertices=[(-r / 1.5, -0.4), (-r / 8, -0.4), (-3 * r / 8, -0.8)],
                                           density=0.5,
                                           friction=8)
        self.left_leg.CreatePolygonFixture(vertices=[(-r / 1.5, 0.4), (-r / 8, 0.4), (-3 * r / 8, 0.8)],
                                           density=0.5,
                                           friction=8)
        self.add_part(self.left_leg)
        joint_left_leg = game.world.CreateRevoluteJoint(bodyA=self.left_leg,
                                                        bodyB=self.left_shoulder,
                                                        localAnchorA=(r - 0.4, 0),
                                                        localAnchorB=(0, 0))
        joint_left_leg.limitEnabled = True
        joint_left_leg.upperLimit = pi / 8
        joint_left_leg.lowerLimit = - pi / 8

        self.right_shoulder = cdb(position=self.position + Vec2(0, r - 0.4),
                                  shapes=b2.b2PolygonShape(box=(0.4, 0.4)))

        game.world.CreateRevoluteJoint(bodyA=self.right_shoulder,
                                       bodyB=self.body,
                                       localAnchorA=(0, 0),
                                       localAnchorB=(0, r - 0.4))
        self.add_part(self.right_shoulder)

        self.right_leg = cdb(position=self.position + Vec2(r, r - 0.4), angle=angle)
        self.right_leg.CreatePolygonFixture(
            vertices=[(-r / 1.5, 0.4), (r / 1.5, 0.4), (r / 1.5, -0.4), (-r / 1.5, -0.4)],
                                            density=1.5,
                                            friction=8)
        self.right_leg.CreatePolygonFixture(vertices=[(r / 1.5, -0.4), (r / 8, -0.4), (3 * r / 8, -0.8)],
                                            density=0.5,
                                            friction=8)
        self.right_leg.CreatePolygonFixture(vertices=[(r / 1.5, 0.4), (r / 8, 0.4), (3 * r / 8, 0.8)],
                                            density=0.5,
                                            friction=8)
        self.add_part(self.right_leg)
        joint_right_leg = game.world.CreateRevoluteJoint(bodyA=self.right_leg,
                                                         bodyB=self.body,
                                                         collideConnected=False,
                                                         localAnchorA=(-r + 0.4, 0),
                                                         localAnchorB=(0, -0.4 + r))

        joint_right_leg.limitEnabled = True
        joint_right_leg.upperLimit = pi / 8
        joint_right_leg.lowerLimit = - pi / 8

    def event(self, event):
        Personage.event(self, event)

    def move(self, direction=1):
        self.body.ApplyTorque(self.speed * direction * self.radius, wake=True)

    def draw(self):
        Personage.draw(self)

    def update(self):
        Personage.update(self)