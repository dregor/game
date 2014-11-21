import pygame
from pygame.locals import *
import Box2D as B2
from gameobject import GameObject
from geometry import Geo
from bits_masks import Bits
from Box2D import b2Vec2 as Vec2


class Maw(GameObject):
    inside_obj = []
    outside_obj = []
    inside = []
    outside = []
    radius = 0
    gravity = 1.1
    n = 0
    speed = 60000
    MOVE_LEFT = False
    MOVE_RIGHT = False

    def __init__(self, game, position=(0, 0), angle=0, radius=10, n=3):
        GameObject.__init__(self, game, position, angle, image='images/default.png')
        self.center_box = self.game.world.CreateStaticBody(
            position=position,
            shapes=B2.b2PolygonShape(box=(0.5, 0.5))
        )
        for item in self.center_box.fixtures:
            item.filterData.maskBits = Bits.NOTHING_MASK
            item.filterData.categoryBits = Bits.NOTHING_BITS

        self.game.world.CreateRevoluteJoint(bodyA=self.body,
                                            bodyB=self.center_box,
                                            anchor=position)
        self.recreate(radius, n)
        for item in self.body.fixtures:
            item.filterData.maskBits = Bits.FULL_MASK
            item.filterData.categoryBits = Bits.FULL_BITS

    def recreate(self, radius, n):
        self.radius = radius
        if n < 3:
            n = 3
        self.n = n
        for f in self.body.fixtures:
            self.body.DestroyFixture(f)
        for vertices in self._polyhedron_full(r=radius, n=n):
            fixture = B2.b2FixtureDef(
                shape=B2.b2PolygonShape(vertices=vertices),
                density=50,
                friction=5,
            )
            self.body.CreateFixture(fixture)

    def _polyhedron_full(self, r=1, n=5):
        outside = Geo.polyhedron(r + 2, n)
        outside.append(outside[0])
        inside = Geo.polyhedron(r, n)
        inside.append(inside[0])
        self.inside[:] = []
        self.outside[:] = []
        for i in range(n):
            self.inside.append((inside[i], inside[i + 1]))
            self.outside.append((outside[i], outside[i + 1]))
            yield [outside[i], outside[i + 1], inside[i + 1], inside[i]]

    def _place(self, i=0, is_inside=True):
        if is_inside:
            pts = self.inside[i]
        else:
            pts = self.outside[i]
        x1, y1 = self.body.transform * pts[0]
        x2, y2 = self.body.transform * pts[1]
        return Geo.center((x1, y1), (x2, y2))

    def add_body(self, child, is_inside=True):
        import random
        from math import pi

        child.is_inside = is_inside

        i = random.randint(0, len(self.body.fixtures) - 1)
        pt = self._place(i, is_inside)
        angle = Geo.angle_to_centre(self.get_position(), Geo.quarter(self.get_position(), pt), pt)

        if is_inside:
            additive = child.additive
            child.angle = 2 * pi - angle
        else:
            child.angle = pi - angle
            additive = tuple(map(lambda (x): x * -1, child.additive))

        child.set_position(Geo.additive(2 * pi - angle, pt, additive))

    def event(self, event):
        if event.type == KEYDOWN:
            key = pygame.key.get_pressed()
            if key[K_PAGEUP]:
                self.recreate(self.radius + 1, self.n + 1)

            if key[K_PAGEDOWN]:
                self.recreate(self.radius - 1, self.n - 1)

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

    def draw(self):
        if self.game.debug:
            for i in range(len(self.body.fixtures)):
                pt = self._place(i)
                pygame.draw.circle(self.game.screen, (20, 20, 20), self.game.to_screen(pt),
                                   int(10 * self.game.camera.zoom), 1)
                pt = self._place(i, False)
                pygame.draw.circle(self.game.screen, (20, 20, 20), self.game.to_screen(pt),
                                   int(10 * self.game.camera.zoom), 1)
        GameObject.draw(self)

    def update(self):
        if self.MOVE_LEFT:
            self.move()
        if self.MOVE_RIGHT:
            self.move(-1)

        for person in self.game.g_objects:
            if person is not self:
                for item in person.give_all_obj():
                    q = Geo.quarter_direction(self.get_position(), item.get_position())
                    if not person.is_inside:
                        q = Vec2(q) * -1
                    force = Geo.to_centre(self.get_position(), item.get_position())
                    force = force[0] * q[0] * self.gravity, force[1] * q[1] * self.gravity
                    # item.body.ApplyLinearImpulse(force, item.get_position(), wake=True)
        GameObject.update(self)
