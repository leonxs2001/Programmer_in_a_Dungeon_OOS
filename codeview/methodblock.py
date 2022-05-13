import pygame
from codeview.inputfield import InputField
from codeview.codeblock import *
class MethodBlock(CodeBlock):
    id = "method"
    def __init__(self, name="print", representation = "print", parameters = ()):
        self.name = name
        self.representation = representation
        self.parameters = parameters
        self.input_fields = []
        super().__init__()

    def get_original_size(self):
        size = super().get_original_size()

        #calculate new size with the number of parameters
        size += ((size.x * len(self.parameters)) / 2, 0)
        return size

    def build_image(self):
        super().build_image()

        size = self.get_original_size() * self.scale_factor
        
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

                #create the new input fileds only if not existing(is length smaller than amount of parameters)
                if len(self.parameters) > len(self.input_fields):
                    center_y = self.visible_size.y / 2
                    left = next_start_x + text_rect.width + distance_x
                    position_in_image = pygame.Vector2(left, center_y)
                    position = position_in_image + self.position
                    self.input_fields.append(InputField(position))

                next_start_x += parameter_graphical_length
    def adjust_to_parent(self, parent):
        #track the current position adjust to parent and give the movement to the inputfields
        position = self.position
        super().adjust_to_parent(parent)
        movement = self.position - position
        for input_field in self.input_fields:
            input_field.move(movement)
            
    def update_scale_factor(self, scalefactor):
        super().update_scale_factor(scalefactor)
        for input_field in self.input_fields:
            input_field.update_scale_factor(scalefactor)

    def try_to_connect(self, block):
        #todo --> connect also with ValueBlocks !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return super().try_to_connect(block)
    def move(self, movement: pygame.Vector2):
        super().move(movement)
        for input_field in self.input_fields:
            input_field.move(movement)
    
    def draw(self, screen):
        super().draw(screen)
        for input_field in self.input_fields:
            input_field.draw(screen)

    def update(self):
        super().update()
        for input_field in self.input_fields:
            input_field.update()