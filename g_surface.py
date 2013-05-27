import pygame

class G_Surface():
    
    def __init__(self, image = None):
        if image == None:
            self.origin = pygame.Surface((0,0))
            self.origin.set_alpha(0)
        else:
            self.load(image)
            
        self.current = self.origin.copy()
        
    def load(self, image):
        self.origin = pygame.image.load(image).convert_alpha()
        

    def _rotozoom(self, image, angle, zoom):
        from math import degrees
        angle = degrees(angle)
        if angle != 0:
            
            #image.get_rect().width *= zoom
            #image.get_rect().height *= zoom
            #image.get_rect().center = ( image.get_rect().center[0] * zoom,image.get_rect().center[1] * zoom)
         
            #rot_rect = image.get_rect().copy()
            rot_image = pygame.transform.rotozoom(image, angle, zoom)
            rot_rect = rot_image.get_rect().copy()         
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            
            return rot_image
        else: 
            return image
        
    def _zoom(self, image, zoom):
        return image
    
    def transform(self, angle, zoom = 0):
        if self.origin.get_size() != (0,0):
            self.current =  self._rotozoom(self.origin, angle, zoom).copy()