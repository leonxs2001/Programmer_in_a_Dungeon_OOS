from email.mime import image
from turtle import position
import pygame
from codeview.codeblock import *
class MethodBlock(CodeBlock):
    id = "method"
    def __init__(self, name="print", parameters = ()):
        self.name = name
        self.parameters = parameters
        super().__init__()
        self.size += ((self.size.x * len(parameters)) / 2, 0)
        self.build_image(self.size * self.scale_factor)
    
    def build_image(self, size):
        super().build_image(size)
        #draw the top circle with border
        pygame.draw.circle(self.image,INVISIBLE_COLOR,(self.circle_x ,-self.circle_overlap),self.circle_radius)
        pygame.draw.circle(self.image,(0,0,0),(self.circle_x ,-self.circle_overlap),self.circle_radius,width=self.border_size)

        #create methodname visualisation
        font = pygame.font.Font(None, int(30 * self.scale_factor))
        text = font.render(self.name ,True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.centery = self.visible_size.y / 2
        text_rect.left = 10 * self.scale_factor
        self.image.blit(text, text_rect)

        #create parameter visualisation
        if len(self.parameters) > 0:
            new_size = (50 * self.scale_factor,30 * self.scale_factor)
            sur = pygame.Surface(new_size)
            sur.fill((255,255,255))
            pygame.draw.rect(sur, (0,0,0), sur.get_rect().copy(), width=self.border_size)
            param_graphical_length = self.visible_size.x / (len(self.parameters) + 1)
            next_position =  pygame.Vector2(param_graphical_length, self.visible_size.y / 2)
            distance = pygame.Vector2(10 * self.scale_factor,0)

            for parameter in self.parameters:
                text = font.render(parameter+":",True, (0,0,0))
                self.image.blit(text, next_position - (0,text.get_size()[1] / 2))
                self.image.blit(sur, next_position + (text.get_size()[0], -new_size[1]/2) +distance)
                next_position.x += param_graphical_length