import random

import pygame
from pygame.locals import *
import Box2D

from g_object import g_object


class Maw(g_object):
    inside_obj = []
    outside_obj = []
    inside = []
    outside = []
    radius = 0
    n = 0
    speed = 100000
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, radius=10, n=3):
        g_object.__init__(self, game, position, angle)
        self.center_box = self.game.world.CreateStaticBody(
            position=position,
            shapes=Box2D.b2PolygonShape(box=(0.1, 0.1))
        )

        self.game.world.CreateRevoluteJoint(bodyA=self.body, bodyB=self.center_box, anchor=position)
        self.recreate(radius, n)

    def recreate(self, radius, n):
        self.radius = radius
        if n < 3: n = 3
        self.n = n
        for f in self.body.fixtures:
            self.body.DestroyFixture(f)
        for vertices in self._polyhedron_full(r=radius, n=n):
            fixture = Box2D.b2FixtureDef(
                shape=Box2D.b2PolygonShape(vertices=vertices),
                density=5,
                friction=0.6,
            )
            self.body.CreateFixture(fixture)

    def _polyhedron(self, r, n):
        from math import cos, sin, pi

        vertices = []
        for i in range(n, 0, -1):
            random.seed(n * random.random() * 10000)
            r_new = r + random.random() * 4
            vertices.append((r_new * sin(2 * i * pi / n), r_new * cos(2 * i * pi / n)))
        return vertices

    def _polyhedron_full(self, r=1, n=5):
        outside = self._polyhedron(r + 2, n)
        outside.append(outside[0])
        inside = self._polyhedron(r, n)
        inside.append(inside[0])
        self.inside[:] = []
        self.outside[:] = []
        for i in range(n):
            self.inside.append((inside[i], inside[i + 1]))
            self.outside.append((outside[i], outside[i + 1]))
            yield [outside[i], outside[i + 1], inside[i + 1], inside[i]]

    def _place(self, i=0, inside=True):
        if inside:
            pts = self.inside[i]
        else:
            pts = self.outside[i]
        x1, y1 = self.body.transform * pts[0]
        x2, y2 = self.body.transform * pts[1]
        return (
            (max((x1, x2)) - min((x1, x2))) / 2 + min((x1, x2)), (max((y1, y2)) - min((y1, y2))) / 2 + min((y1, y2)))

    def _additive(self, alpha, pt, add):
        from math import sin, cos, pi

        dx = pt[0] + cos(2 * pi - alpha) * add[0] + sin(2 * pi - alpha) * add[1]
        dy = pt[1] + cos(2 * pi - alpha) * add[1] - sin(2 * pi - alpha) * add[0]
        return dx, dy

    def _quarter(self, pt):
        pt = (pt[0] - self.position[0], pt[1] - self.position[1])
        if pt[0] > 0:
            if pt[1] > 0:
                return 1
            else:
                return 2
        else:
            if pt[1] > 0:
                return 4
            else:
                return 3

    def _length(self, pt1, pt2):
        from math import sqrt, pow
        return sqrt(pow(pt2[0] - pt1[0], 2) + pow(pt2[1] - pt1[1], 2))

    def _angle_to(self, q, pt):
        from math import pi
        if q == 1:
            return pi + self._alpha(pt)
        elif q == 2:
            return 2 * pi - self._alpha(pt)
        elif q == 3:
            return self._alpha(pt)
        elif q == 4:
            return pi - self._alpha(pt)

    def _alpha(self, A):
        from math import asin
        if A == (0.0, 0.0):
            return 0
        else:
            A = (A[0] - self.position[0], A[1] - self.position[1])
            return asin(self._length((0, 0), (A[0], 0)) / self._length(A, (0, 0)))

    def add_body(self, child, inside=True):
        import random
        from math import pi

        i = random.randint(0, len(self.body.fixtures) - 1)
        pt = self._place(i, inside)
        angle = self._angle_to(self._quarter(pt), pt)

        if inside:
            additive = child.additive
            child.body.angle = 2 * pi - angle
        else:
            child.body.angle = pi - angle
            additive = tuple(map(lambda (x): x * -1, child.additive))

        child.body.position = self._additive(2 * pi - angle, pt, additive)

    def _to_centre(self, pt):
        from math import pi, cos, degrees
        c = self._length((0, 0), pt)
        betha = self._alpha(pt)
        alpha = pi/2 - betha
        return c * cos(alpha), c * cos(betha)

    def event(self, event):
        if event.type == KEYDOWN:
            key = pygame.key.get_pressed()
            if key[K_PAGEUP]:
                self.recreate(self.radius + 0.5, self.n + 1)

            if key[K_PAGEDOWN]:
                self.recreate(self.radius - 0.5, self.n - 1)

            if key[K_LEFT]:
                self.MOVE_LEFT = True

            if key[K_RIGHT]:
                self.MOVE_RIGHT = True

        if event.type == KEYUP:
            if event.key == K_LEFT:
                self.MOVE_LEFT = False

            if event.key == K_RIGHT:
                self.MOVE_RIGHT = False

    def move(self, direction=1):
        import platform

        if "windows" in platform.system():
            self.body.ApplyTorque(self.speed * direction * self.radius)
        else:
            self.body.ApplyTorque(self.speed * direction * self.radius, wake=True)

    def draw(self):
        if self.game.debug:
            for i in range(len(self.body.fixtures)):
                pt = self._place(i)
                pygame.draw.circle(self.game.screen, (150, 150, 150), self.game.to_screen(pt),
                                   int(10 * self.game.camera.zoom), 1)
                pt = self._place(i, False)
                pygame.draw.circle(self.game.screen, (150, 150, 150), self.game.to_screen(pt),
                                   int(10 * self.game.camera.zoom), 1)
        g_object.draw(self)

    def update(self):
        if self.MOVE_LEFT:
            self.move(-1)
        if self.MOVE_RIGHT:
            self.move()
        for item in self.game.g_objects:
            if item is not self:
                q = self._quarter(item.position)
                if q == 1:
                    q = (1, 1)
                elif q == 2:
                    q = (1, -1)
                elif q == 3:
                    q = (-1, -1)
                elif q == 4:
                    q = (-1, 1)

                if not item.is_inside:
                    q = q[0] * -1, q[1] * -1

                force = self._to_centre(item.position)
                force = force[0] * 5 * q[0], force[1] * 5 * q[1]
                item.body.ApplyLinearImpulse(force, item.position, wake=True)
        g_object.update(self)
