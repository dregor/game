import pygame,sys
from pygame.locals import *
from bactery import Bactery
from pygame.color import *
from debug import Debuger

class Game():
    game_name = 'Game'
    playing = False
    g_objects = []
    fps = 60
    dt = 1./fps
    debug = True

    def __init__(self):
        pygame.init()
        self.debuger = Debuger(self)
        self.font = pygame.font.SysFont('Arial',12)
        self.screen = pygame.display.set_mode((640,320))
        pygame.display.set_caption(self.game_name)
        self.clock = pygame.time.Clock()
        self.g_objects.append( Bactery(self) )

    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def text_out(self, color, size, text):
        if pygame.font:
            font = pygame.font.Font(None, size)
            text = font.render(text, 4, color )
            textpos = text.get_rect()
            textpos.center = self.screen.get_rect().center
            screen.blit(text, textpos)

    def start(self):
        self.playing = True

    def stop(self):
        slef.playing = False

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
        self.clock.tick(self.fps)
        for item in self.g_objects:
            item.update()

game = Game()
game.start()

while True:
    game.event()
    if game.playing == True:
        game.update()
    game.draw()
