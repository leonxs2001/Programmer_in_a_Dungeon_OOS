from multiprocessing.sharedctypes import Value
import pygame
from codeview.block import Block
from codeview.inputfield import InputField
class ValueBlock(Block):
    size_y = 30
    text_space_x = InputField.empty_size.x * 1.5
    distance_x = 7
    def __init__(self, background_color = (20,200,20), name = "+", representation = "+", parameters = ("Zahl1", "Zahl2")):
        self.name = name
        self.representation = representation
        self.parameters = parameters
        self.input_fields = []
        self.texts = []
        self.name_text = pygame.Surface((10,10))
        super().__init__(background_color)
        
    def get_size(self):
        size = pygame.Vector2(0, ValueBlock.size_y * self.scale_factor)
        size.x += len(self.input_fields) * ValueBlock.distance_x * 2 * self.scale_factor
        size.x += self.name_text.get_size()[0]
        for input_field in self.input_fields:
            size.x += input_field.get_size().x
        for text in self.texts:
            size.x += text[0].get_width()
        return size.copy()
        
    def build_image(self):
        
        next_start_x = 0
        size = pygame.Vector2(0, ValueBlock.size_y * self.scale_factor)
        self.texts = []

        #create methodname visualisation
        font = pygame.font.Font(None, int(25 * self.scale_factor))
        self.name_text = font.render(self.name ,True, (0,0,0))
        name_text_rect = self.name_text.get_rect()
        name_text_rect.centery = size.y / 2
        name_text_rect.left = ValueBlock.distance_x * self.scale_factor

        #create parameter visualisation
        if len(self.parameters) > 0:
            #calculate the start position
            next_start_x = ValueBlock.distance_x * self.scale_factor * 2
            next_start_x += self.name_text.get_size()[0]
            i = 0
            for parameter in self.parameters :
                #create and save the current textimage with the parametername and its rect 
                text = font.render(parameter+":",True, (0,0,0))
                text_rect = text.get_rect()
                text_rect.centery = size.y / 2
                text_rect.left = next_start_x
                self.texts.append((text.copy(), text_rect.copy()))
                next_start_x += text.get_width() + ValueBlock.distance_x * self.scale_factor

                #create the new input fileds only if not existing(is length smaller than amount of parameters)
                if len(self.parameters) > len(self.input_fields):
                    center_y = size.y / 2 
                    left = next_start_x
                    position_in_image = pygame.Vector2(left, center_y)
                    position = position_in_image + self.position
                    input_field = InputField(position)
                    self.input_fields.append(input_field)
                    next_start_x += input_field.get_size().x  
                else:
                    print(self.input_fields[i] ,self.input_fields[i].get_size())
                    next_start_x += self.input_fields[i].get_size().x

                next_start_x += ValueBlock.distance_x * self.scale_factor
            i+=1

        next_start_x -= ValueBlock.distance_x * self.scale_factor
        size.x = next_start_x

        self.image = pygame.Surface(size)
        self.image.fill(self.background_color)
        pygame.draw.rect(self.image, (0,0,0), pygame.rect.Rect((0,0), size), width=2)
        self.rect = self.image.get_rect()

        #blit the name
        self.image.blit(self.name_text, name_text_rect)
    
        #blit the texts
        for text in self.texts:
            self.image.blit(text[0], text[1])

    def adjust_to_input_field(self, input_field):
        old_position = self.position
        self.position = input_field.left_center - (0, (ValueBlock.size_y * self.scale_factor) / 2)
        #also move the input fields to the new correct position
        for input_field in self.input_fields:
            input_field.move(self.position - old_position)

    def append(self, value_block):#ändern!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.input_fields[0].append(value_block)

    def update_scale_factor(self, scalefactor):
        for input_field in self.input_fields:
            input_field.update_scale_factor(scalefactor)
        super().update_scale_factor(scalefactor)

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
