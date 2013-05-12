import pygame
import Box2D
from pygame.locals import *
from pygame.color import *

class DebugDraw():
    circle_segments = 16
    surface = None

    def __init__(self, game):
        super(fwDebugDraw, self).__init__()
        self.surface = game.surface
        self.game = game

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

    def to_screen(self, pt):
        return ((pt[0] * self.viewZoom) - self.viewOffset.x, self.height - ((pt[1] * self.viewZoom) - self.viewOffset.y))


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

    def draw(self):
        x, y = pygame.mouse.get_pos()
        self.game.screen.blit( self.game.font.render('fps : ' + str(self.game.clock.get_fps()), 1, THECOLORS['red']), self.position )
        self.game.screen.blit( self.game.font.render('mouse : ' + str(x) + ',' + str(y), 1, THECOLORS['red']), (self.position[0],self.position[1]+14) )

    def update(self):
        pass
