from composite import Composite
from Box2D import b2Vec2 as Vec2
from gameobject import GameObject
from math import pi


class Circle(GameObject):
    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, radius=1, image='images/default.png', density=20,
                 friction=8, name='Circle'):
        GameObject.__init__(self, game, position=position, angle=angle, is_inside=is_inside, image=image)
        size = self.surface.origin.get_size()
        self.name = name
        self.radius = ((size[0] + size[1]) / 4) / game.PPM
        self.body.CreateCircleFixture(radius=radius,
                                      density=density,
                                      friction=friction)

    def move(self, speed=10, direction=1):
        self.body.ApplyTorque(speed * direction * self.radius, wake=True)

    def mirror(self, orientation=(1, 1)):
        pass


class Rectangle(GameObject):
    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, size=(1, 0.4), image='images/default.png',
                 density=20, friction=8, name='Rect'):
        GameObject.__init__(self, game, position=position, angle=angle, is_inside=is_inside, image=image)
        width, height = size
        self.name = name
        self.body.CreatePolygonFixture(
            vertices=[(-width / 2, height / 2),
                      (width / 2, height / 2),
                      (width / 2, -height / 2),
                      (-width / 2, -height / 2)],
            density=density,
            friction=friction)

    def mirror(self, orientation=(1, 1)):
        pass


class FixtureObject(GameObject):
    def __init__(self,
                 game,
                 position=(0, 0),
                 angle=0,
                 is_inside=True,
                 image='images/default.png',
                 vertices=[(-2, -1), (2, -1), (0, 1)],
                 density=20,
                 friction=8,
                 name='Fixture'):

        self.density = density
        self.friction = friction
        self.name = name
        GameObject.__init__(self, game, position=position, angle=angle, is_inside=is_inside, image=image)
        self.body.CreatePolygonFixture(
            vertices=vertices,
            density=density,
            friction=friction)

    def mirror(self, orientation=(-1, 1)):
        cb = 0
        gi = 0
        mi = 0
        fixtures = []
        for i in self.body.fixtures:
            vertices = []
            for j in i.shape.vertices:
                vertices.append(Vec2(j[0] * orientation[0], j[1] * orientation[1]))
            fixtures.append(vertices)
            cb = i.filterData.categoryBits
            gi = i.filterData.groupIndex
            mi = i.filterData.maskBits
            self.body.DestroyFixture(i)
        print(fixtures)
        for i in fixtures:
            fixture = self.body.CreatePolygonFixture(vertices=i,
                                                     density=self.density,
                                                     friction=self.friction)
            fixture.filterData.categoryBits = cb
            fixture.filterData.groupIndex = gi
            fixture.filterData.maskBits = mi

    def draw(self):
        GameObject.draw(self)

class MonkeyHand(Composite):
    def __init__(self, game, position=(0, 0), angle=0, is_inside=True, size=(1, 0.4), name='Hand'):
        width, height = size
        Composite.__init__(self, game, position, angle, is_inside=is_inside, name=name,
                           body=Rectangle(game,
                                          position=position,
                                          angle=angle,
                                          is_inside=is_inside,
                                          size=(height, height)))

        self.shoulder = self.body
        vertices = [(-width / 2, 0),
                    (-width / 4, height),
                    (0, height / 2),
                    (width / 2, height / 2),
                    (width / 2, -height / 2),
                    (-width / 4, -height)]

        forearm_pos = Vec2(position) + Vec2(-width / 2 + height / 2, 0)
        forearm_joint_pos = (width / 2 - height / 2, 0)

        self.forearm = FixtureObject(game,
                                     position=forearm_pos,
                                     angle=angle,
                                     is_inside=is_inside,
                                     vertices=vertices,
                                     name='forearm')

        self.add_part(self.forearm)
        '''
        self.forearm_joint = game.world.CreateRevoluteJoint(bodyA=self.forearm.body,
                                                            bodyB=self.shoulder.body,
                                                            collideConnected=False,
                                                            localAnchorA=forearm_joint_pos,
                                                            localAnchorB=(0, 0))

        self.joints.append(self.forearm_joint)

        self.forearm_joint.limitEnabled = True
        self.forearm_joint.upperLimit = pi / 8
        self.forearm_joint.lowerLimit = - pi / 8
        '''

    def event(self, event):
        Composite.event(self, event)

    def move(self, direction=1):
        pass

    def draw(self):
        Composite.draw(self)

    def update(self):
        Composite.update(self)
