import pygame,sys
from pygame.locals import *
from camera import Camera
from bactery import Bactery
from maw import Maw
from debug import Debuger
import Box2D

class Game():
    GAME_NAME = 'Polyhedron'

    @property
    def center( self ):
        return self.screen.get_rect().center

    WIDTH, HEIGHT = 800, 600
    PPM  = 20.
    FPS = 60
    TIME_STEP = 1./FPS

    g_objects = []

    playing = False
    debug = True

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial',12)
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)
        self.clock = pygame.time.Clock()
        self.camera = Camera(self,offset = (self.center[0]*-1,self.center[1]*-1))
        aabb = Box2D.b2AABB()
        aabb.lowerBound = (-100,-100)
        aabb.upperBound = (100,100)
        self.world = Box2D.b2World(worldAABB = aabb, gravity=(0,-25), doSleep=True)
        self.debuger = Debuger(self)
        #self.beneath()
        self.test2()

    def to_screen(self, pt):
        return (int((pt[0] * self.PPM * self.camera.zoom) - self.camera.offset[0]),
                int( self.HEIGHT - ((pt[1]* self.PPM * self.camera.zoom) - self.camera.offset[1])))

    def to_world(self, pt):
        return ( ((pt[0] + self.camera.offset[0]) / self.camera.zoom) / self.PPM,
                 ((self.HEIGHT - pt[1] + self.camera.offset[1])/self.camera.zoom)/self.PPM)

    def test2(self):

        self.g_objects.append( Maw(self, position = (0,0), radius= 10, n = 6 ))
        self.g_objects.append( Bactery(self,(-0.5,0)))

    def test1(self):
        self.g_objects.append( Bactery(self, self.to_world((200,140)) ) )
        self.ground_body = self.world.CreateStaticBody(
                                                       position=self.to_world((320,440)),
                                                       shapes = [Box2D.b2PolygonShape(box=(10,1)),
                                                                 Box2D.b2PolygonShape(vertices=[(0,1),(-10,5),(-10,1)])
                                                                 ]
                                                       )
    def beneath(self):
        vertex = [ [(10,self.HEIGHT-self.HEIGHT/10),
                    (10,self.HEIGHT-self.HEIGHT/20)],
                   [(10,self.HEIGHT-self.HEIGHT/20),
                    (self.WIDTH-self.WIDTH/10,self.HEIGHT-self.HEIGHT/20)],
                   [(self.WIDTH-self.WIDTH/10,self.HEIGHT-self.HEIGHT/20),
                    (self.WIDTH-self.WIDTH/10,self.HEIGHT-self.HEIGHT/10)]
                 ]
        vertex = [ [ self.to_world(pt) for pt in vert ] for vert in vertex ]
        self.world.CreateStaticBody(
                shapes=[ Box2D.b2EdgeShape(vertices=vertex[0]),
                         Box2D.b2EdgeShape(vertices=vertex[1]),
                         Box2D.b2EdgeShape(vertices=vertex[2])
                         ],
                position=(1,0))

    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_F1:
                if self.debug:
                    self.debug = False
                else:
                    self.debug = True

            if event.type == KEYDOWN and event.key == K_j:
                    maw = self.g_objects[0]
                    obj =  self.g_objects[1]
                    maw.addBody( obj )

            if event.type == KEYDOWN and event.key == K_p:
                if self.playing:
                    self.playing = False
                else:
                    self.playing= True

            self.camera.event(event)

            for obj in self.g_objects:
                obj.event(event)


    def start(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def draw(self):
        background = pygame.Surface(self.screen.get_size()).convert()
        background.fill((24, 36, 27))
        self.screen.blit(background,(0,0))

        for item in self.g_objects:
            item.draw()

        if self.debug:
            self.debuger.draw()
            self.debuger.text_out('zoom :' + str(self.camera.zoom) +' - '+ str(self.camera.zoom_level),(2,44))

        pygame.display.flip()
        pygame.display.update()

    def update(self):
        self.world.Step(self.TIME_STEP,10,10)
        for item in self.g_objects:
            item.update()
        self.clock.tick(self.FPS)

game = Game()
game.start()
try:
    while True:
        game.event()
        if game.playing == True:
            game.update()
        game.draw()
except KeyboardInterrupt:
    print('KeyInt')
