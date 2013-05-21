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
        

    def _rotate(self, image, angle):
        from math import degrees
        angle = degrees(angle)
        if angle != 0:
            orig_rect = image.get_rect()
            rot_image = pygame.transform.rotate(image, angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            return rot_image
        else: 
            return image
        
    def _zoom(self, image, zoom):
        return image
    
    def transform(self, angle, zoom = 0):
        if self.origin.get_size() != (0,0):
            self.current = self._zoom( self._rotate(self.origin, angle), zoom).copy()