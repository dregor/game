import pygame
from Box2D import *
from pygame.locals import *
from pygame.color import *

class DebugDraw(b2Draw):
    circle_segments = 16
    surface = None

    def __init__(self, game):
        super(DebugDraw, self).__init__()
        self.surface = game.screen
        self.game = game
        self.viewZoom =1.
        self.viewOffset = (0,0)
        self.width, self.height = game.SCREEN_WIDTH, game.SCREEN_HEIGHT
        
    def StartDraw(self): pass

    def EndDraw(self): pass
    
    def DrawPoint(self, p, size, color):
        self.DrawCircle(p, size, color, drawwidth=0)

    def DrawAABB(self, aabb, color):
        points = [self.to_screen(p) for p in [
                    (aabb.lowerBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.upperBound.y ),
                    (aabb.lowerBound.x, aabb.upperBound.y ),
                    ] ]
        pygame.draw.aalines(self.surface, color, True, points)

    def DrawSegment(self, p1, p2, color):
        pygame.draw.aaline(self.surface, color.bytes, self.to_screen(p1), self.to_screen(p2))

    def DrawTransform(self, xf):
        p1 = xf.position
        p2 = self.to_screen(p1 + 0.4 * xf.R.col1)
        p3 = self.to_screen(p1 + 0.4 * xf.R.col2)
        p1 = self.to_screen(p1)

        pygame.draw.aaline(self.surface, (255,0,0), p1, p2)
        pygame.draw.aaline(self.surface, (0,255,0), p1, p3)

    def DrawCircle(self, center, radius, color, drawwidth=1):
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.to_screen(center)
        pygame.draw.circle(self.surface, color.bytes, center, radius, drawwidth)

    def DrawSolidCircle(self, center_v, radius, axis, color):
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.to_screen(center_v)
        pygame.draw.circle(self.surface, (color/2).bytes+[127], center, radius, 0)

        pygame.draw.circle(self.surface, color.bytes, center, radius, 1)

        p = radius * axis
        pygame.draw.aaline(self.surface, (255,0,0), center, (center[0] - p.x, center[1] + p.y))

    def DrawPolygon(self, in_vertices, vertexCount, color):
        if len(in_vertices) == 2:
            pygame.draw.aaline(self.surface, color.bytes, self.to_screen(in_vertices[0]), self.to_screen(in_vertices[1]))
        else:
            pygame.draw.polygon(self.surface, color.bytes, [self.to_screen(v) for v in in_vertices], 1)

    def DrawSolidPolygon(self, in_vertices, vertexCount, color):
        if len(in_vertices) == 2:
            pygame.draw.aaline(self.surface, color.bytes, self.to_screen(in_vertices[0]), self.to_screen(in_vertices[1]))
        else:
            vertices = [self.to_screen(v) for v in in_vertices]
            pygame.draw.polygon(self.surface, (color/2).bytes+[127], vertices, 0)
            pygame.draw.polygon(self.surface, color.bytes, vertices, 1)

    def DrawCircleShape(self, shape, transform, color):
        pass
    
    def DrawPolygonShape(self, shape, transform, color):
        pass

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
            pass # don't draw it here
        else:
            self.DrawSegment(x1, p1, color)
            self.DrawSegment(p1, p2, color)
            self.DrawSegment(x2, p2, color)
            
    def ManualDraw(self):

        colors = {
            'active'    : b2Color(0.5, 0.5, 0.3),
            'static'    : b2Color(0.5, 0.9, 0.5), 
            'kinematic' : b2Color(0.5, 0.5, 0.9), 
            'asleep'    : b2Color(0.6, 0.6, 0.6), 
            'default'   : b2Color(0.9, 0.7, 0.7), 
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
                for childIndex in range(shape.childCount):
                    self.DrawAABB(shape.getAABB(transform, childIndex), color)

    def to_screen(self, pt):
        return ((pt[0] * self.viewZoom) - self.viewOffset[0], self.height - ((pt[1] * self.viewZoom) - self.viewOffset[1]))


class Debuger():
    _position = (0,0)

    @property
    def position( self ):
        return self._position
    @position.setter
    def position(self, val):
        self._position = val

    def __init__(self, game):
        
        self.game = game
        self.font = pygame.font.SysFont('Arial',12)
        self.DebugDraw = DebugDraw(self.game)
        self.game.world.renderer = self.DebugDraw

    def draw(self):
        x, y = pygame.mouse.get_pos()
        self.DebugDraw.ManualDraw()
        self.game.screen.blit( self.game.font.render('fps : ' + str(self.game.clock.get_fps()), 1, THECOLORS['red']), self.position )
        self.game.screen.blit( self.game.font.render('mouse : ' + str(x) + ',' + str(y), 1, THECOLORS['red']), (self.position[0],self.position[1]+14) )

    def update(self):
        pass
