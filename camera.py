from pygame.locals import *
class Camera():
    zoom = 1.
    zoom_level = 0

    def event(self, event):
            if event.type == KEYDOWN and event.key == K_w:
                 self.offset = (self.offset[0],self.offset[1]+10)

            if event.type == KEYDOWN and event.key == K_s:
                 self.offset = (self.offset[0],self.offset[1]-10)

            if event.type == KEYDOWN and event.key == K_a:
                 self.offset = (self.offset[0]-10,self.offset[1])

            if event.type == KEYDOWN and event.key == K_d:
                 self.offset = (self.offset[0]+10,self.offset[1])

            if event.type == KEYDOWN and event.key == K_q:
                 self.set_zoom(self.zoom_level + 1)

            if event.type == KEYDOWN and event.key == K_e:
                 self.set_zoom(self.zoom_level - 1)

    def set_zoom(self,val):
        if val == 0:
            self.zoom = 1.
        elif val < 0:
            self.zoom = 1/(-1.*val+1)
        else:
            self.zoom = val+1
        self.zoom_level = val

    def __init__(self, game, offset =(0,0), angle = 0, zoom_level = 0):
        self.game = game
        self.offset = offset
        self.angle = angle
        self.set_zoom(zoom_level)

