import pygame,sys
from pygame.locals import *
angle = 0
def rotate(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image,angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center 
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def polyhedron(pos, r, n):
    from math import cos, sin, pi
    vertices = []
    for i in range(0,n):
        vertices.append( (pos[0] + (r *sin(2*i*pi/n)),pos[1] + (r * cos(2*i*pi/n))) )
    return vertices

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
image = 'images/sprite.bmp'
sprite = pygame.image.load(image).convert_alpha()
while True:
    for i in range(0,360,10):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        clock.tick(60)
        background = pygame.Surface(screen.get_size()).convert()
        background.fill((250, 250, 250))
        screen.blit(background,(0,0))
        screen.blit(  rotate(sprite,i), (320,240) ) 
        pygame.draw.polygon(screen, (200,100,100), polyhedron((320,240),100,5) , 1)
        pygame.display.flip()
        pygame.display.update()