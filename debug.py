import pygame
from Box2D import *
from pygame.locals import *
from pygame.color import *

class DebugDraw():

    def __init__(self, game):
        self.surface = game.screen
        self.game = game
        self.Zoom =1.
        self.Offset = (0,0)
        self.width, self.height = game.WIDTH, game.HEIGHT

    def DrawPoint(self, p, size, color):
        pygame.draw.circle(self.surface, color, center, 1, 0)

    def DrawAABB(self, aabb, color):
        points = [self.game.to_screen(p) for p in [
                    (aabb.lowerBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.upperBound.y ),
                    (aabb.lowerBound.x, aabb.upperBound.y ),
                    ] ]
        pygame.draw.aalines(self.surface, color, True, points)

    def DrawSegment(self, p1, p2, color):
        pygame.draw.aaline(self.surface, color.bytes, self.game.to_screen(p1), self.game.to_screen(p2))

    def DrawTransform(self, xf):
        p1 = xf.position
        p2 = self.game.to_screen(p1 + 0.4 * xf.R.col1)
        p3 = self.game.to_screen(p1 + 0.4 * xf.R.col2)
        p1 = self.game.to_screen(p1)

        pygame.draw.aaline(self.surface, (255,0,0), p1, p2)
        pygame.draw.aaline(self.surface, (0,255,0), p1, p3)

    def DrawSolidCircle(self, center_v, radius, angle, color):
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.game.to_screen(center_v)
        pygame.draw.circle(self.surface, color, center, radius, 0)
        pygame.draw.circle(self.surface, (220,220,220), center, radius+2, 2)

        pygame.draw.aaline( self.surface, (100,120,100), center, self.axis(angle, radius, center) )

    def axis(self, angle, radius, center ):
        from math import cos,sin
        return b2Vec2(center[0] + sin(angle) * radius, center[1] + cos(angle) * radius)

    def DrawCircleShape(self, shape, transform, color):
        self.DrawSolidCircle(b2Vec2(transform*shape.pos), int(shape.radius*self.game.PPM*self.game.camera.zoom),transform.angle, color.bytes)

    def DrawPolygonShape(self, shape, transform, color):
        vertices=[(transform*v) for v in shape.vertices]
        vertices = map(self.game.to_screen,vertices)
        pygame.draw.polygon(self.surface, color.bytes, vertices)
        pygame.draw.polygon(self.surface, (0,0,0), vertices, 1)

    def DrawShape(self, shape, transform, color):
        if isinstance(shape, b2PolygonShape):
            self.DrawPolygonShape(shape, transform, color)
        elif isinstance(shape, b2EdgeShape):
            v1=b2Mul(transform, shape.vertex1)
            v2=b2Mul(transform, shape.vertex2)
            self.DrawSegment(v1, v2, color)
        elif isinstance(shape, b2CircleShape):
            self.DrawCircleShape(shape, transform, color)
        elif isinstance(shape, b2LoopShape):
            vertices=shape.vertices
            v1=b2Mul(transform, vertices[-1])
            for v2 in vertices:
                v2=b2Mul(transform, v2)
                self.DrawSegment(v1, v2, color)
                v1=v2

    def DrawJoint(self,joint):
        bodyA, bodyB=joint.bodyA, joint.bodyB
        xf1, xf2=bodyA.transform, bodyB.transform
        x1, x2=xf1.position, xf2.position
        p1, p2=joint.anchorA, joint.anchorB
        color=b2Color(0.5, 0.8, 0.8)

        if isinstance(joint, b2DistanceJoint):
            self.DrawSegment(p1, p2, color)
        elif isinstance(joint, b2PulleyJoint):
            s1, s2=joint.groundAnchorA, joint.groundAnchorB
            self.DrawSegment(s1, p1, color)
            self.DrawSegment(s2, p2, color)
            self.DrawSegment(s1, s2, color)

        elif isinstance(joint, b2MouseJoint):
            pass
        else:
            self.DrawSegment(x1, p1, color)
            self.DrawSegment(p1, p2, color)
            self.DrawSegment(x2, p2, color)

    def ManualDraw(self):

        colors = {
            'active'    : b2Color(0.25, 0.35, 0.25),
            'static'    : b2Color(0.25, 0.25, 0.35),
            'kinematic' : b2Color(0.35, 0.25, 0.35),
            'asleep'    : b2Color(0.55, 0.45, 0.41),
            'default'   : b2Color(0.63, 0.62, 0.61),
        }

        for body in self.game.world.bodies:
                transform=body.transform
                for fixture in body.fixtures:
                    shape=fixture.shape

                    if not body.active: color=colors['active']
                    elif body.type==b2_staticBody: color=colors['static']
                    elif body.type==b2_kinematicBody: color=colors['kinematic']
                    elif not body.awake: color=colors['asleep']
                    else: color=colors['default']

                    self.DrawShape(fixture.shape, transform, color)

        for joint in self.game.world.joints:
            self.DrawJoint(joint)

        color=b2Color(0.9, 0.3, 0.9)

        for body in self.game.world.bodies:
            if not body.active:
                continue
            transform=body.transform
            for fixture in body.fixtures:
                shape=fixture.shape
                #for childIndex in range(shape.childCount):
                #   self.DrawAABB(shape.getAABB(transform, childIndex), color)

class Debuger():

    def __init__(self, game):
        self.game = game
        self.DebugDraw = DebugDraw(self.game)

    def text_out(self, text, pt, color = THECOLORS['red'], size = 14 ):
        if pygame.font:
            font = self.game.font
            text = font.render(text, 4, color )
            #textpos = text.get_rect()
            #textpos.center = pt
            self.game.screen.blit(text, pt)

    def draw(self):
        pos = pygame.mouse.get_pos()
        self.DebugDraw.ManualDraw()
        self.text_out('fps : ' + str(self.game.clock.get_fps()), (2,2) )
        self.text_out('mouse : ' + str(pos), (2,16) )
        self.text_out('mouse (world): ' + str(self.game.to_world(pos)), (2,30) )

    def update(self):
        pass
