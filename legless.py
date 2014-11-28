from personage import Personage
from Box2D import b2Vec2 as Vec2
from personage_parts import MonkeyHand, Circle
from random import sample
from math import pi


class LegLess(Personage):
    images = ['images/ameb.gif', 'images/bakt.gif', 'images/microb.gif']

    def __init__(self, game, position=(0, 0), angle=0, name='', speed=2000, is_you=False, is_inside=True):
        body = Circle(game,
                      position=position,
                      is_inside=is_inside,
                      image=sample(self.images, 1)[0])

        r = body.radius

        self.additive = (0, r)

        Personage.__init__(self,
                           game=game,
                           position=position,
                           angle=angle,
                           name=name,
                           speed=speed,
                           is_you=is_you,
                           is_inside=is_inside,
                           body=body)

        self.left_hand = MonkeyHand(game, position=self.get_position() + Vec2(0, 2 * 0.4 - r), is_inside=is_inside,
                                    size=(r, 0.4), name='leftHand')
        self.add_part(self.left_hand)

        '''
        self.left_hand_joint = game.world.CreateRevoluteJoint(bodyA=self.left_hand.shoulder.body,
                                                              bodyB=self.body.body,
                                                              localAnchorA=(0, 0),
                                                              localAnchorB=(0, 2 * 0.4 - r))
        self.joints.append(self.left_hand_joint)
        self.left_hand_joint.limitEnabled = True
        '''

        self.right_hand = MonkeyHand(game, position=self.get_position() + Vec2(0, r - 2 * 0.4),
                                     is_inside=is_inside,
                                     size=(r, 0.4),
                                     name='RightHand')
        self.right_hand.mirror(orientation=(-1, -1))
        self.add_part(self.right_hand)

        '''
        self.right_hand_joint = game.world.CreateRevoluteJoint(bodyA=self.right_hand.shoulder.body,
                                                               bodyB=self.body.body,
                                                               localAnchorA=(0, 0),
                                                               localAnchorB=(0, r - 2 * 0.4))

        self.joints.append(self.right_hand_joint)
        self.right_hand_joint.limitEnabled = True
        '''

    def event(self, event):
        Personage.event(self, event)

    def move(self, direction=1):
        Personage.move(self, direction)
        # self.body.move(direction=direction, speed=self.speed)

    def draw(self):
        Personage.draw(self)

    def update(self):
        Personage.update(self)