import pygame
import copy
from codeview.block.twosidedblock import TwoSidedBlock
from codeview.block.valueblock import ValueBlock
from codeview.block.inputfield import InputField
from codeview.block.codeblock import *

class MethodBlock(TwoSidedBlock):
    distance_x = 7
    def __init__(self, name="print", representation = "print", parameters = ()):
        self.name = name
        self.representation = representation
        self.parameters = parameters
        self.input_fields = []
        super().__init__()
        if len(self.parameters) == 2:
            self.input_fields[0].id = "sp"

    def __copy__(self):
        #overwrite the copy method
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        new_input_fields = []
        for input_field in self.input_fields:
            new_input_fields.append(copy.copy(input_field))
        result.input_fields = new_input_fields
        return result

    def get_size(self):
        return self.size 

    def build(self):

        next_start_x = 0
        self.size = pygame.Vector2(0, CodeBlock.size.y * self.scale_factor )
        texts = []

        #create methodname visualisation
        name_text = self.render_text(self.name)
        name_text_rect = name_text.get_rect()
        name_text_rect.centery = self.size.y / 2
        name_text_rect.left = MethodBlock.distance_x * self.scale_factor
        #create parameter visualisation
        if len(self.parameters) > 0:
            #calculate the start for the parameter(length of the name text + the space bewteen)
            next_start_x = MethodBlock.distance_x * self.scale_factor * 2
            next_start_x += name_text.get_size()[0]

            i = 0
            for parameter in self.parameters :
                #create and save the current textimage with the parametername and its rect 
                text = self.render_text(parameter)
                text_rect = text.get_rect()
                text_rect.centery = self.size.y / 2
                text_rect.left = next_start_x
                texts.append((text.copy(), text_rect.copy()))#can blit if the backgroundsurface exist
                next_start_x += text.get_width() + MethodBlock.distance_x * self.scale_factor

                #calculate the position for the current inputfield and create it
                center_y = self.size.y / 2 
                left = next_start_x
                position_in_image = pygame.Vector2(left, center_y)
                position = position_in_image + self.position
                #create the new input fileds only if not existing(is length smaller than amount of parameters)
                if len(self.parameters) > len(self.input_fields):
                    input_field = InputField(position)
                    self.input_fields.append(input_field)
                    next_start_x += input_field.get_size().x  
                else:
                    #update the position
                    self.input_fields[i].left_center = position
                    self.input_fields[i].adjust_block_to_input_field()
                    #if the input fields already exist add theire width
                    next_start_x += self.input_fields[i].get_size().x
                #add the space between text and inputfield
                next_start_x += MethodBlock.distance_x * self.scale_factor
                i += 1   

        #set the width of the whole Surface to the Endposition
        self.size.x = next_start_x

        #scale the Methodblock to normal Codeblock size if it is to small
        distance = CodeBlock.size.x * self.scale_factor - self.size.x
        if distance > 0:
            self.size.x += distance
            for i, input_field in enumerate(self.input_fields):
                texts[i][1].left += distance
                input_field.move(pygame.Vector2(distance,0))

        #create background surface
        super().build()

        #blit the name(now we have the SUrface to blit on))
        self.image.blit(name_text, name_text_rect)
    
        #blit the texts with the rect(both in a tuper)
        for text in texts:
            self.image.blit(text[0], text[1])
                
    def rebuild(self):
        """Rebuild self and all input_fields"""
        for input_field in self.input_fields:
            input_field.rebuild()
        self.build()
        self.adjust_to_parent()
        self.adjust_blocks()

    def give_keyboard_down_event(self, event):
        super().give_keyboard_down_event(event)
        for input_field in self.input_fields:#give it to the Input fields
            input_field.give_keyboard_down_event(event)

    def render_text(self, text):
        font = pygame.font.Font(None, int(25 * self.scale_factor))
        return font.render(text + ":" ,True, (0,0,0)) 

    def adjust_to_parent(self):
        #track the current position adjust to parent and give the movement to the inputfields
        position = self.position
        super().adjust_to_parent()
        movement = self.position - position
        for input_field in self.input_fields:
            input_field.move(movement)
            
    def update_scale_factor(self, scalefactor):
        for input_field in self.input_fields:
            input_field.update_scale_factor(scalefactor)
        super().update_scale_factor(scalefactor)     

    def try_to_connect(self, block):
        #only connect with the input fild if the given block is a value block
        if isinstance(block, ValueBlock):
            
            for input_field in self.input_fields:
                appended = input_field.try_to_connect(block)
                if appended:
                    self.rebuild()
                    return appended

        return super().try_to_connect(block)

    def get_collider(self, mouse_position: pygame.Vector2):
        #go through the inputfields and check if they colliding with the mouse
        for input_field in self.input_fields:
            #delete the selected block frm line and return it for adding into the blockview blocklist
            collider = input_field.get_collider(mouse_position)
            if collider:
                if collider == input_field.value:
                    input_field.value = "1"
                    input_field.rebuild()
                self.rebuild()
                collider.rebuild()
                return collider

        return super().get_collider(mouse_position)

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
    def get_code_string(self):
        result = f".{self.representation}("
        for input_field in self.input_fields:
            result += input_field.get_code_string() + ","
        if len(self.input_fields) != 0:
            result = result[:-1]#delete last ,
        result += ")"
        result += super().get_code_string()
        return result