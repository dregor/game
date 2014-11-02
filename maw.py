import pygame
from pygame.locals import *

import Box2D

from g_object import g_object

from geometry import geo


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

    def _polyhedron_full(self, r=1, n=5):
        outside = geo.polyhedron(r + 2, n)
        outside.append(outside[0])
        inside = geo.polyhedron(r, n)
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
        return geo.center((x1, y1), (x2, y2))

    def add_body(self, child, inside=True):
        import random
        from math import pi

        i = random.randint(0, len(self.body.fixtures) - 1)
        pt = self._place(i, inside)
        angle = geo.angle_to_centre(self.position, geo.quarter(self.position, pt), pt)

        if inside:
            additive = child.additive
            child.body.angle = 2 * pi - angle
        else:
            child.body.angle = pi - angle
            additive = tuple(map(lambda (x): x * -1, child.additive))

        child.body.position = geo.additive(2 * pi - angle, pt, additive)

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
        self.body.ApplyTorque(self.speed * direction * self.radius, wake=True)
        """
        import platform
        if "windows" in platform.system():
            self.body.ApplyTorque(self.speed * direction * self.radius)
        else:"""

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
                q = geo.quarter_direction(self.position, item.position)
                if not item.is_inside:
                    q = q[0] * -1, q[1] * -1
                force = geo.to_centre(self.position, item.position)
                force = force[0] * 5 * q[0], force[1] * 5 * q[1]
                item.body.ApplyLinearImpulse(force, item.position, wake=True)
        g_object.update(self)
