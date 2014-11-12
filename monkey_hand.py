from composite import Composite
import Box2D as b2
from Box2D import b2Vec2 as Vec2
from g_object import G_Object
from math import pi


class Shoulder(G_Object):
    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, size=(1, 0.4)):
        G_Object.__init__(self, game, position=position, angle=angle, is_inside=is_inside, image='images/default.png')
        width, height = size
        self.body.CreateFixturesFromShapes(b2.b2PolygonShape(box=(height, height)))
        self.body.density = 0.001


class Forearm(G_Object):
    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, size=(1, 0.4)):
        G_Object.__init__(self, game, position=position, angle=angle, is_inside=is_inside, image='images/default.png')
        width, height = size
        self.body.CreatePolygonFixture(
            vertices=[(-width / 2, height / 2),
                      (width / 2, height / 2),
                      (width / 2, -height / 2),
                      (-width / 2, -height / 2)],
            density=1.5,
            friction=8)
        '''
        self.body.CreatePolygonFixture(vertices=[(-width / 2, height/2),
                                                 (-width / 4, 1.5 * height),
                                                 (0, height/2)],
                                       density=0.001,
                                       friction=8)
        self.body.CreatePolygonFixture(vertices=[(-width / 2, -height/2),
                                                 (-width / 4, -1.5 * height),
                                                 (0, -height/2)],
                                       density=0.001,
                                      friction=8)
        '''


class Hand(Composite):
    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, size=(1, 0.4)):
        Composite.__init__(self, game, position, angle, is_inside=is_inside)
        width, height = size

        self.shoulder = Shoulder(game, position=position, angle=angle, is_inside=is_inside)
        self.add_part(self.shoulder)

        self.forearm = Forearm(game, position=self.position + Vec2(height / 2 - width / 2, 0), angle=angle,
                               is_inside=is_inside)
        self.add_part(self.forearm)

        self.forearm_joint = game.world.CreateRevoluteJoint(bodyA=self.forearm.body,
                                                            bodyB=self.shoulder.body,
                                                            collideConnected=False,
                                                            localAnchorA=(width / 2 - height / 2, 0),
                                                            localAnchorB=(0, 0))

        self.forearm_joint.limitEnabled = True
        self.forearm_joint.upperLimit = pi / 8
        self.forearm_joint.lowerLimit = - pi / 8


    def event(self, event):
        Composite.event(self, event)

    def move(self, direction=1):
        pass

    def draw(self):
        Composite.draw(self)

    def update(self):
        Composite.update(self)
