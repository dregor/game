import pygame
from pygame.locals import *
import Box2D
from g_object import G_Object

class Maw(G_Object):
    inside_obj = []
    outside_obj = []
    inside = []
    outside = []
    radius = 0
    n = 0
    
    def __init__(self, game, position = (0,0), angle=0, radius = 10, n = 3 ):
        G_Object.__init__(self, game, position, angle)
        self.center_box = self.game.world.CreateStaticBody(
                                                    position=position,
                                                    shapes = Box2D.b2PolygonShape(box=(0.1,0.1))
                                                )

        self.game.world.CreateRevoluteJoint(bodyA=self.body,bodyB=self.center_box,anchor = position )
        self.recreate(radius, n)

    def recreate(self, radius, n):
        self.radius = radius
        if n < 3: n = 3
        self.n = n
        for f in self.body.fixtures:
            self.body.DestroyFixture(f)
        for vertices in self._polyhedron_full( r = radius, n = n ):
            fixture=Box2D.b2FixtureDef(
                    shape=Box2D.b2PolygonShape(vertices=vertices),
                    density=5,
                    friction=0.6,
                    )
            self.body.CreateFixture(fixture)
        #self.body.SetMassFromShapes()

    def _polyhedron(self, r , n ):
        from math import cos, sin, pi
        vertices = []
        for i in range(n,0,-1):
            vertices.append(( r *sin(2*i*pi/n),r * cos(2*i*pi/n) ))
        return vertices

    def _polyhedron_full(self, r =1, n= 5):
        outside = self._polyhedron( r + 2, n )
        outside.append(outside[0])
        inside = self._polyhedron( r, n )
        inside.append(inside[0])
        self.inside[:]=[]
        self.outside[:]=[]
        for i in range(n):
            self.inside.append((inside[i],inside[i+1]))
            self.outside.append((outside[i],outside[i+1]))
            yield [ outside[i], outside[i+1], inside[i+1], inside[i] ]

    def _place(self, i = 0 ):
        #fixture = self.body.fixtures[i]
        #ver = self._near( fixture.shape.vertices )
        pts = self.inside[i]
        x1,y1 = self.body.transform*pts[0]
        x2,y2 = self.body.transform*pts[1]
        return ( (max((x1,x2))-min((x1,x2)))/2+min((x1,x2)), (max((y1,y2))-min((y1,y2)))/2+min((y1,y2)))

    def _additive(self, alpha, pt, add):
        from math import sin, cos, pi
        dx = pt[0] + cos(2*pi-alpha) * add[0] + sin(2*pi-alpha) * add[1]
        dy = pt[1] + cos(2*pi-alpha) * add[1] - sin(2*pi-alpha) * add[0]
        return( dx, dy )

    def _near( self, pt_array ):
        length = {}
        for pt in pt_array:
            ptf = (float("%.10f"%pt[0]),float("%.10f"%pt[1]))
            length.update( { float("%.10f"%self._length(ptf, self.position)):ptf } )
        sor = sorted(length)
        return (length[sor[0]],length[sor[1]])

    def _quarter(self,pt):
        pt = (pt[0] - self.position[0], pt[1] - self.position[1])
        if( pt[0] > 0):
            if(pt[1]>0):
                return 1
            else:
                return 2
        else:
            if(pt[1] > 0):
                return 4
            else:
                return 3

    def _length(self, pt1, pt2):
        from math import sqrt,pow
        return  sqrt(pow(pt2[0]-pt1[0],2)+pow(pt2[1]-pt1[1],2))


    def _alpha(self, A):
        from math import asin
        A = (A[0] - self.position[0], A[1] - self.position[1])
        return asin(self._length((0,0),(A[0],0))/self._length(A,(0,0)))

    def addBody(self, child):
        import random
        from math import pi
        i = random.randint(0,len(self.body.fixtures)-1)
        pt = self._place(i)
        q = self._quarter(pt)
        if q == 1:
            angle = pi+self._alpha(pt)
        elif q == 2:
            angle = 2*pi-self._alpha(pt)
        elif q == 3:
            angle = self._alpha(pt)
        elif q == 4:
            angle = pi-self._alpha(pt)

        child.body.angle = 2*pi - angle
        child.body.position = self._additive( 2*pi-angle,  pt, child.additive )

    def event(self, event):
            if event.type == KEYDOWN and event.key == K_PAGEUP:
                self.recreate( self.radius + 0.5, self.n + 1 )

            if event.type == KEYDOWN and event.key == K_PAGEDOWN:
                self.recreate( self.radius - 0.5, self.n - 1 )

            if event.type == KEYDOWN and event.key == K_LEFT:
                self.body.ApplyTorque(-100000 * self.radius)

            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.body.ApplyTorque(100000 * self.radius)

    def draw(self):
        for i in range(len(self.body.fixtures)):
            pt = self._place(i)
            pygame.draw.circle(self.game.screen, (150,150,150), self.game.to_screen(pt) , 10, 1)
        '''
            q = self._quarter(pt)
            self.game.debuger.text_out((255,255,255),16,str(q)+str((round(pt[0]),round(pt[1]))),self.game.to_screen(pt))
        for fixture in self.body.fixtures:
            i=0
            for point in fixture.shape.vertices:
                i+=1
                pt = self.body.transform*point
                pt = (int(pt[0]),int(pt[1]))
                pygame.draw.circle(self.game.screen, (10,40*i,10), self.game.to_screen(pt) , 6, 6)
                self.game.debuger.text_out((255,255,255),16,str(i)+':'+str(pt),self.game.to_screen(pt))
        '''
        G_Object.draw(self)


    def update(self):
        G_Object.update(self)

