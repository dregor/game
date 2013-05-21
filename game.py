import pygame,sys
from pygame.locals import *
from bactery import Bactery
from maw import Maw
from debug import Debuger

from Box2D.b2 import world,polygonShape
import Box2D

class Game():
    GAME_NAME = 'Game'
    
    @property
    def centr( self ):
        return (self.WIDTH/2,self.HEIGHT/2)

    WIDTH, HEIGHT=640,480
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
        self.world = world(gravity=(0,-10),doSleep=True)
        self.debuger = Debuger(self)

        self.test1()
        
    def to_screen(self, pt):
        return (int(pt[0] * self.PPM ),int( self.HEIGHT - pt[1]* self.PPM ))
    
    def to_world(self, pt):

        return ( pt[0] / self.PPM, 
                           (self.HEIGHT - pt[1])/self.PPM)
    
    def test1(self):
        self.g_objects.append( Maw(self, position = self.to_world((320,240)), n =8 ) )
        self.world.CreateStaticBody(
                shapes=[ Box2D.b2EdgeShape(vertices=[(0,2),(0,1)]),
                         Box2D.b2EdgeShape(vertices=[(0,1),(30,1)]),
                         Box2D.b2EdgeShape(vertices=[(30,1),(30,2)])
                         ],
                position=(1,0)
            )
        self.g_objects.append( Bactery(self, self.to_world((250,140)) ) )
        self.ground_body = self.world.CreateStaticBody(
                                                       position=self.to_world((320,440)),
                                                       shapes = [polygonShape(box=(10,1)),
                                                                 polygonShape(vertices=[(0,1),(-10,5),(-10,1)])
                                                                 ]
                                                       )
        
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

            if event.type == KEYDOWN and event.key == K_p:
                if self.playing:
                    self.playing = False
                else:
                    self.playing= True

    def text_out(self, color, size, text):
        if pygame.font:
            font = pygame.font.Font(None, size)
            text = font.render(text, 4, color )
            textpos = text.get_rect()
            textpos.center = self.screen.get_rect().center
            self.screen.blit(text, textpos)

    def start(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def draw(self):
        background = pygame.Surface(self.screen.get_size()).convert()
        background.fill((200, 105, 105))
        self.screen.blit(background,(0,0))

        for item in self.g_objects:
            item.draw()

        if self.debug:
            self.debuger.draw()

        pygame.display.flip()
        pygame.display.update()

    def update(self):
        self.world.Step(self.TIME_STEP,10,10)
        for item in self.g_objects:
            item.update()
        self.clock.tick(self.FPS)

game = Game()
game.start()

while True:
    game.event()
    if game.playing == True:
        game.update()
    game.draw()
