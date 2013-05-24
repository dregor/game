import pygame
import Box2D
from g_object import G_Object

class Maw(G_Object):
    inside_obj = []
    outside_obj = []

    def __init__(self, game, position = (0,0), angle=0, radius = 10, n = 3 ):
        G_Object.__init__(self, game, position, angle)
        for vertices in self._polyhedron_full( r = radius, n = n ):
            fixture=Box2D.b2FixtureDef(
                    shape=Box2D.b2PolygonShape(vertices=vertices),
                    density=1,
                    friction=0.6,
                    )
            self.body.CreateFixture(fixture)
        self.center = self.game.world.CreateStaticBody(
                                                    position=position,
                                                    shapes = Box2D.b2PolygonShape(box=(1,1))
                                                )

        joint = self.game.world.CreateRevoluteJoint(bodyA=self.body,bodyB=self.center,anchor = self.body.worldCenter )


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
        for i in range(n):
            yield [ outside[i], outside[i+1], inside[i], inside[i+1] ]

    def _place(self, i = 0):
        from math import cos,sin,pi
        fixture = self.body.fixtures[i]
        x1,y1 = self.body.transform*fixture.shape.vertices[0]
        x2,y2 = self.body.transform*fixture.shape.vertices[3]
        return ( (max((x1,x2))-min((x1,x2)))/2+min((x1,x2)), (max((y1,y2))-min((y1,y2)))/2+min((y1,y2)))

    def _quarter(self,pt):
        pt = (pt[0] - self.position[0], pt[1] - self.position[1])
        if( pt[0] > 0):
            if(pt[1]>0):
                return 1
            else:
                return 2
        else:
            if(pt[1]>0):
                return 3
            else:
                return 4

    def _length(self, pt1, pt2):
        from math import modf,sqrt,pow
        return sqrt(pow(pt2[0]-pt1[0],2)+pow(pt2[1]-pt1[1],2))

    def _alpha(self, A):
        from math import asin
        #A = (A[0] - self.position[0], A[1] - self.position[1])
        print('a = '+str(self._length(A,(A[0],0))))
        print('c = '+str(self._length(A,(0,0))))
        return asin(self._length(A,(A[0],0))/self._length(A,(0,0)))

    def addBody(self, childBody):
        import random
        from math import pi,degrees
        #i = random.randint(0,len(self.body.fixtures)-1)
        i = 0
        pt = self._place(i)
        childBody.body.position = pt
        q = self._quarter(pt)
        print('A = '+str(pt))
        if q == 1:
            angle = pi+self._alpha(pt)
        elif q == 2:
            angle = 2*pi-self._alpha(pt)
        elif q == 3:
            angle = 2*pi+self._alpha(pt)
        elif q == 4:
            angle = pi-self._alpha(pt)
        print('alpha = '+str(degrees(angle)))
        childBody.body.angle = degrees(angle)

    def draw(self):
        import pygame
        pt = self._place(0)
        pt = self.game.to_screen(( pt[0], pt[1]))
        pygame.draw.circle(self.game.screen, (150,150,150), pt , 10, 10)
        for fixture in [self.body.fixtures[0]]:
            i=0
            for point in fixture.shape.vertices:
                i+=1
                pt = self.body.transform*point
                pt = (int(pt[0]),int(pt[1]))
                pygame.draw.circle(self.game.screen, (10,40*i,10), self.game.to_screen(pt) , 6, 6)
                self.game.text_out((255,255,255),16,str(i)+':'+str(pt),self.game.to_screen(pt))
        G_Object.draw(self)


    def update(self):
        G_Object.update(self)

