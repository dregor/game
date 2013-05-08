import pygame,sys
from pygame.locals import *
from bactery import Bactery
from debug import Debuger

import Box2D
from Box2D.b2 import *

class Game():
    GAME_NAME = 'Game'
        
    SCREEN_WIDTH, SCREEN_HEIGHT=640,480
    PPM  = 20.
    FPS = 60
    TIME_STEP = 1./FPS
    
    g_objects = []
    
    playing = False
    debug = True

    def __init__(self):
        pygame.init()
        self.debuger = Debuger(self)
        self.font = pygame.font.SysFont('Arial',12)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)
        self.clock = pygame.time.Clock()
        self.world = world(gravity=(0,-10),doSleep=True)
        self.g_objects.append( Bactery(self,(10,15)) )
        self.ground_body = self.world.CreateStaticBody(
                                                       position=(0,1),
                                                       shapes = polygonShape(box=(50,5))
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
        background.fill((250, 250, 250))
        self.screen.blit(background,(0,0))

        for item in self.g_objects:
            item.draw()

        if self.debug:
            self.debuger.draw()

        pygame.display.flip()
        pygame.display.update()

    def update(self):
        self.clock.tick(self.FPS)
        self.world.Step(self.TIME_STEP,10,10)
        for item in self.g_objects:
            item.update()

game = Game()
game.start()

while True:
    game.event()
    if game.playing == True:
        game.update()
    game.draw()
    
