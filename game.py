import sys
import pygame
from pygame.locals import *

import Box2D as b2

from camera import Camera
from debug import debuger
from test2 import test2, test1


class QueryCallback(b2.b2QueryCallback):
    def __init__(self, p):
        super(QueryCallback, self).__init__()
        self.point = p
        self.fixture = None

    def ReportFixture(self, fixture):
        body = fixture.body
        if body.type == b2.b2_dynamicBody:
            inside = fixture.TestPoint(self.point)
            if inside:
                self.fixture = fixture
                return False
        return True


class Game():
    GAME_NAME = 'Polyhedron'

    @property
    def center(self):
        return self.screen.get_rect().center

    WIDTH, HEIGHT = 1024, 768
    PPM = 20.
    FPS = 40
    TIME_STEP = 1. / FPS

    g_objects = []

    playing = False
    debug = True
    mouse_joint = None

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 14)
        self.font.set_bold(True)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)
        self.clock = pygame.time.Clock()
        self.camera = Camera(self, offset=(self.center[0] * -1, self.center[1] * -1))
        aabb = b2.b2AABB()
        aabb.lowerBound = (-100, -100)
        aabb.upperBound = (100, 100)
        self.world = b2.b2World(worldAABB=aabb, gravity=(0, 0), doSleep=True)
        self.debuger = debuger(self)
        self.maw = None
        test2(self)

    def to_screen(self, pt):
        return (int((pt[0] * self.PPM * self.camera.zoom) - self.camera.offset[0]),
                int(self.HEIGHT - ((pt[1] * self.PPM * self.camera.zoom) - self.camera.offset[1])))

    def to_world(self, pt):
        return (((pt[0] + self.camera.offset[0]) / self.camera.zoom) / self.PPM,
                ((self.HEIGHT - pt[1] + self.camera.offset[1]) / self.camera.zoom) / self.PPM)

    def mouse_down(self, pt):
        if self.mouse_joint is not None:
            return
        aabb = b2.b2AABB(lowerBound=(pt[0] - 0.001, pt[1] - 0.001), upperBound=(pt[0] + 0.001, pt[1] + 0.001))
        query = QueryCallback(pt)
        self.world.QueryAABB(query, aabb)
        if query.fixture:
            body = query.fixture.body

            self.joint_box = self.world.CreateStaticBody(
                position=pt,
                shapes=b2.b2PolygonShape(box=(0.3, 0.3)))

            for item in self.joint_box.fixtures:
                item.filterData.maskBits = 0x0003
                item.filterData.categoryBits = 0x0000

            self.mouse_joint = self.world.CreateMouseJoint(
                bodyA=self.joint_box,
                bodyB=body,
                target=pt,
                maxForce=1000.0 * body.mass)
            body.awake = True

    def mouse_up(self):
        if self.mouse_joint is not None:
            self.world.DestroyJoint(self.mouse_joint)
            self.world.DestroyBody(self.joint_box)
            self.mouse_joint = None
            self.joint_box = None

    def event(self):
        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down(self.to_world(event.pos))
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_up()
            if event.type == MOUSEMOTION:
                if self.mouse_joint is not None:
                    pt = self.to_world(event.pos)
                    self.joint_box.transform = b2.b2Vec2(pt[0], pt[1]), 0
                    self.mouse_joint.target = pt

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_F1:
                if self.debug:
                    self.debug = False
                else:
                    self.debug = True
            '''
            if event.type == KEYDOWN and event.key == K_i:
                obj = self.g_objects[1]
                obj.is_inside = True
                self.maw.add_body(obj)

            if event.type == KEYDOWN and event.key == K_o:
                obj = self.g_objects[1]
                obj.is_inside = False
                self.maw.add_body(obj, False)
            '''
            if event.type == KEYDOWN and event.key == K_p:
                if self.playing:
                    self.playing = False
                else:
                    self.playing = True

            self.camera.event(event)

            for obj in self.g_objects:
                obj.event(event)

    def start(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def draw(self):
        background = pygame.Surface(self.screen.get_size()).convert()
        background.fill((143, 243, 240))
        self.screen.blit(background, (0, 0))

        for item in self.g_objects:
            item.draw()

        if self.debug:
            self.debuger.draw()
            self.debuger.text_out('zoom :' + str(self.camera.zoom) + ' - ' + str(self.camera.zoom_level), (2, 44))

        '''
        for obj in self.g_objects:
            rect = obj.surface.current.get_rect(center = obj.position,x = obj.position[0])
            pos = self.to_screen(obj.position)
            pygame.draw.rect( self.screen, (0,0,0), pygame.Rect((pos[0]-rect.width/2,pos[1]-rect.height/2),rect.size), 1)
        '''

        pygame.display.flip()
        pygame.display.update()

    def update(self):
        self.world.Step(self.TIME_STEP, 8, 6)

        for item in self.g_objects:
            item.update()
        self.clock.tick(self.FPS)
        self.camera.update()


game = Game()
game.start()
try:
    while True:
        game.event()
        if game.playing is True:
            game.update()
        game.draw()
except KeyboardInterrupt:
    print('KeyInt')
