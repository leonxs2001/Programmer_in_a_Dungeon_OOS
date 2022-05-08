import pygame
from codeview.codeblock import *
class MethodBlock(CodeBlock):
    def __init__(self):
        super().__init__()
        self.position = self.position = pygame.Vector2(400, 337) - (self.size / 2)
    
    def build_image(self, size):
        super().build_image(size)
        #draw the top circle with border
        pygame.draw.circle(self.image,INVISIBLE_COLOR,(self.circle_x ,-self.circle_overlap),self.circle_radius)
        pygame.draw.circle(self.image,(0,0,0),(self.circle_x ,-self.circle_overlap),self.circle_radius,width=self.border_size)