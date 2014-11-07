from bactery import Bactery
from legless import LegLess
from maw import Maw
from math import pi
import Box2D as b2


def test3(game):
    game.maw = Maw(game, position=(0, 0), radius=10, n=6)
    game.g_objects.append(game.maw)

    game.legless = LegLess(game, (0, 0), name='leg0')
    game.maw.add_body(game.legless, is_inside=False)
    app = game.g_objects.append
    app(game.legless)


def test2(game):
    game.maw = Maw(game, position=(0, 0), radius=15, n=10)
    game.g_objects.append(game.maw)

    game.bactery1 = Bactery(game, (0, 5), name='b1')
    game.bactery2 = Bactery(game, (5, 0), name='b2')
    game.bactery3 = Bactery(game, (0, -25), name='b3', is_you=True, is_inside=False)
    game.bactery4 = Bactery(game, (-5, 0), name='b4')

    game.legless = LegLess(game, (0, 0), name='leg0')
    game.maw.add_body(game.legless, is_inside=False)
    app = game.g_objects.append

    app(game.legless)
    app(game.bactery1)
    app(game.bactery2)
    app(game.bactery3)
    app(game.bactery4)

    game.bactery1.body.fixtures[0].filterData.maskBits = 0x0001 + 0x0002
    game.bactery2.body.fixtures[0].filterData.maskBits = 0x0001 + 0x0002
    game.bactery3.body.fixtures[0].filterData.maskBits = 0x0004 + 0x0001
    game.bactery4.body.fixtures[0].filterData.maskBits = 0x0004 + 0x0001

    game.bactery1.body.fixtures[0].filterData.categoryBits = 0x0002
    game.bactery2.body.fixtures[0].filterData.categoryBits = 0x0002
    game.bactery3.body.fixtures[0].filterData.categoryBits = 0x0004
    game.bactery4.body.fixtures[0].filterData.categoryBits = 0x0004

    joint_name = 'revolute'

    if joint_name == 'distance':
        game.world.CreateDistanceJoint(bodyA=game.bactery1.body,
                                       bodyB=game.bactery2.body,
                                       length=15,
                                       frequency=10)

    elif joint_name == 'prismatic':
        game.world.CreatePrismaticJoint(bodyA=game.bactery1.body,
                                        bodyB=game.bactery2.body,
                                        localAnchorA=(0, 1),
                                        localAnchorB=(0, -1),
                                        # referenceAngle=pi/2,
                                        enableLimit=True,
                                        lowerTranslation=3,
                                        upperTranslation=6)

    elif joint_name == 'wheel':
        game.world.CreateWheelJoint(bodyA=game.bactery1.body,
                                    bodyB=game.bactery2.body,
                                    collideConnected=True)

        game.world.joints[1].springDampingRatio = 10000

    elif joint_name == 'pulley':
        game.world.CreatePulleyJoint(bodyA=game.bactery1.body,
                                     bodyB=game.bactery2.body,
                                     groundAnchorA=(0, 0),
                                     groundAnchorB=(0, 0),
                                     lengthA=3,
                                     lengthB=6,
                                     ratio=2)

    elif joint_name == 'weld':
        game.world.CreateWeldJoint(bodyA=game.bactery1.body,
                                   bodyB=game.bactery2.body,
                                   localAnchorA=(0, - game.bactery1.radius),
                                   localAnchorB=(0, game.bactery2.radius))

    elif joint_name == 'friction':
        game.world.CreateFrictionJoint(bodyA=game.bactery1.body,
                                       bodyB=game.bactery2.body,
                                       collideConnected=True,
                                       maxForce=10000,
                                       maxTorque=10000)

    elif joint_name == 'rope':
        game.world.CreateRopeJoint(bodyA=game.bactery1.body,
                                   bodyB=game.bactery2.body,
                                   maxLength=7,
                                   localAnchorA=(0, - game.bactery1.radius),
                                   localAnchorB=(0, game.bactery2.radius))

    elif joint_name == 'revolute':
        game.world.CreateRevoluteJoint(bodyA=game.bactery1.body,
                                       bodyB=game.bactery2.body,
                                       collideConnected=True,
                                       localAnchorA=(0, - game.bactery1.radius * 1.5),
                                       localAnchorB=(0, game.bactery2.radius * 1.5))

        game.world.joints[1].limitEnabled = True
        game.world.joints[1].lowerLimit = - pi / 2
        game.world.joints[1].upperLimit = pi / 2

    elif joint_name == 'gear':
        pass


def beneath(game):
    vertex = [[(10, game.HEIGHT - game.HEIGHT / 10),
               (10, game.HEIGHT - game.HEIGHT / 20)],
              [(10, game.HEIGHT - game.HEIGHT / 20),
               (game.WIDTH - game.WIDTH / 10, game.HEIGHT - game.HEIGHT / 20)],
              [(game.WIDTH - game.WIDTH / 10, game.HEIGHT - game.HEIGHT / 20),
               (game.WIDTH - game.WIDTH / 10, game.HEIGHT - game.HEIGHT / 10)]
    ]
    vertex = [[game.to_world(pt) for pt in vert] for vert in vertex]
    game.world.CreateStaticBody(
        shapes=[b2.b2EdgeShape(vertices=vertex[0]),
                b2.b2EdgeShape(vertices=vertex[1]),
                b2.b2EdgeShape(vertices=vertex[2])],
        position=(1, 0))


def test1(game):
    game.g_objects.append(Bactery(game, game.to_world((200, 140))))
    game.ground_body = game.world.CreateStaticBody(
        position=game.to_world((320, 440)),
        shapes=[b2.b2PolygonShape(box=(10, 1)),
                b2.b2PolygonShape(vertices=[(0, 1), (-10, 5), (-10, 1)])])