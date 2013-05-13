import pygame
from Box2D.b2 import *

class Bactery():
    image = 'images/microb.gif'
    _position = (0,0)
    debug_vertices = []
    @property
    def position( self ):
        return self._position
    @position.setter
    def position(self, val):
        self._position = val

    def __init__(self, game, position = (0,0) ):
        self.position = position
        self.game = game
        self.sprite = pygame.image.load(self.image).convert_alpha()
        self.body = self.game.world.CreateDynamicBody(position = position, angle=15)
        self.body_circle = self.body.CreateCircleFixture(radius = 2, density=1, friction=0.3)
 
    def draw_circle(self):
        position=self.body.transform*self.body_circle.shape.pos*self.game.PPM
        position=(position[0], self.game.SCREEN_HEIGHT-position[1])
        pygame.draw.circle(self.game.screen, (30,150,40), [int(x) for x in position], int(self.body_circle.shape.radius*self.game.PPM))
        
    def draw(self):
        self.game.screen.blit( self.sprite, ( self.position[0] - self.sprite.get_width()/2, self.position[1]- self.sprite.get_height()/2) )
        #if self.game.debug:
        #    self.draw_circle()
            # pygame.draw.polygon(self.game.screen, (100,100,100), self.debug_vertices)

    def update(self):
        pos = self.body.position*self.game.PPM
        self.position = (pos[0],self.game.SCREEN_HEIGHT - pos[1] )
        '''x, y = pygame.mouse.get_pos()
        for fixture in self.body.fixtures:
            shape = fixture.shape
            vertices = [(self.body.transform*v)*self.game.PPM for v in shape.vertices ]
            self.debug_vertices = [(v[0],self.game.SCREEN_HEIGHT-v[1]) for v in vertices]           
    
        if self.position[0] < x: self.position = ( self.position[0] + 1,self.position[1] )
        if self.position[0] > x: self.position = ( self.position[0] - 1,self.position[1] )
        if self.position[0] < y: self.position = ( self.position[0],self.position[1] + 1 )
        if self.position[0] > y: self.position = ( self.position[0],self.position[1] - 1 )
        '''