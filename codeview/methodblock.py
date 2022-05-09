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

        #set the new size based on the number of parameters
        self.size += ((self.size.x * len(parameters)) / 2, 0)
        #rebuild the image based on the new size
        self.build_image(self.size * self.scale_factor)
    
    def build_image(self, size):
        super().build_image(size)

        #add/draw the top circle with border(makes this block connectable on both sides)
        pygame.draw.circle(self.image, INVISIBLE_COLOR, (self.circle_x ,-self.circle_overlap), self.circle_radius)
        pygame.draw.circle(self.image, (0,0,0), (self.circle_x ,-self.circle_overlap), self.circle_radius, width = 2)

        #create methodname visualisation
        font = pygame.font.Font(None, int(30 * self.scale_factor))
        text = font.render(self.name ,True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.centery = self.visible_size.y / 2
        text_rect.left = 10 * self.scale_factor
        self.image.blit(text, text_rect)

        #create parameter visualisation
        if len(self.parameters) > 0:
            #create the empty white rectangle for the parameters
            new_size = (50 * self.scale_factor,30 * self.scale_factor)
            empty_parameter_surface = pygame.Surface(new_size)
            empty_parameter_surface.fill((255,255,255))
            pygame.draw.rect(empty_parameter_surface, (0,0,0), empty_parameter_surface.get_rect().copy(), width=2) # create the border
            empty_parameter_rect = empty_parameter_surface.get_rect()

            #calculate the length of every parametersection(one parameter sectionlength is half of the normal size)
            parameter_graphical_length = self.visible_size.x / (len(self.parameters) + 1)
            next_start_x = parameter_graphical_length
            distance_x = 10 * self.scale_factor #distance between the parameter text and parameterfield

            for parameter in self.parameters:
                #create and blit the current textimage with the parametername and its rect 
                text = font.render(parameter+":",True, (0,0,0))
                text_rect = text.get_rect()
                text_rect.centery = self.visible_size.y / 2
                text_rect.left = next_start_x
                self.image.blit(text, text_rect)

                #blit the empty white rectangle to the right position
                empty_parameter_rect.centery = self.visible_size.y / 2
                empty_parameter_rect.left = next_start_x + text_rect.width + distance_x
                self.image.blit(empty_parameter_surface, empty_parameter_rect)
                next_start_x += parameter_graphical_length