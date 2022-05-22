import random
import pygame
from codeview.block import Block
from codeview.inputfield import InputField
class ValueBlock(Block):
    size_y = 30
    distance_x = 7
    def __init__(self, name = "+", representation = "+", parameters = ("Zahl1", "Zahl2")):
        background_color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        
        self.name = name
        self.representation = representation
        self.parameters = parameters
        self.input_fields = []
        super().__init__(background_color)

    def get_size(self):
        return self.size

    def build(self):
        
        next_start_x = 0
        self.size = pygame.Vector2(0, ValueBlock.size_y * self.scale_factor)
        texts = []

        #create methodname visualisation
        
        name_text = self.render_text(self.name)
        name_text_rect = name_text.get_rect()
        name_text_rect.centery = self.size.y / 2
        name_text_rect.left = ValueBlock.distance_x * self.scale_factor

        #calculate the start for the parameter(length of the name text + the space bewteen)
        next_start_x = ValueBlock.distance_x * self.scale_factor * 2
        next_start_x += name_text.get_size()[0]
        
        #create parameter visualisation
        if len(self.parameters) > 0:

            i = 0
            for parameter in self.parameters :
                #create and save the current textimage with the parametername and its rect 
                text = self.render_text(parameter)
                text_rect = text.get_rect()
                text_rect.centery = self.size.y / 2
                text_rect.left = next_start_x
                texts.append((text.copy(), text_rect.copy()))#can blit if the backgroundsurface exist
                next_start_x += text.get_width() + ValueBlock.distance_x * self.scale_factor

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
                next_start_x += ValueBlock.distance_x * self.scale_factor
                i+=1   

        #set the width of the whole Surface to the Endposition
        self.size.x = next_start_x

        #create background surface
        self.image = pygame.Surface(self.size)
        self.image.fill(self.background_color)
        pygame.draw.rect(self.image, (0,0,0), pygame.rect.Rect((0,0), self.size), width=2)
        self.rect = self.image.get_rect()

        #blit the name(now we have the SUrface to blit on))
        self.image.blit(name_text, name_text_rect)
    
        #blit the texts with the rect(both in a tuper)
        for text in texts:
            self.image.blit(text[0], text[1])

    def render_text(self, text):
        font = pygame.font.Font(None, int(25 * self.scale_factor))
        return font.render(text + ":" ,True, (0,0,0)) 

    def rebuild(self):
        """Rebuild self and all input_fields"""
        for input_field in self.input_fields:
            input_field.rebuild()
        self.build()

    def give_keyboard_event(self, event):
        for input_field in self.input_fields:#give it to the Input fields
            input_field.give_keyboard_event(event)

    def get_collider(self, mouse_position: pygame.Vector2):
        #go through the inputfields and check if they colliding with the mouse
        for input_field in self.input_fields:
            #delete the selected block frm line and return it for adding into the blockview blocklist
            collider = input_field.get_collider(mouse_position)

            if collider:
                if collider == input_field.value:
                    input_field.value = "1"
                self.rebuild()
                collider.rebuild()
                return collider

        if self.rect.collidepoint(mouse_position):
            self.in_focus = True
            return self

    def try_to_connect(self, block):

        #only connect if the given block is a value block
        if isinstance(block, ValueBlock) and block != self:
            for input_field in self.input_fields:
                appended = input_field.try_to_connect(block)
                if appended:
                    self.rebuild()
                    return appended

    def adjust_to_input_field(self, input_field):
        old_position = self.position
        self.position = input_field.left_center - (0, (ValueBlock.size_y * self.scale_factor) / 2)
        #also move the input fields to the new correct position
        for input_field in self.input_fields:
            input_field.move(self.position - old_position)

    def __str__(self):
        res = "<"+self.name + f" Inputfields:"
        for input in self.input_fields:
            res+= f", {input}"
        res+= f"; Size: {self.get_size()}"
        res+=">"
        return res

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
        #print(self)
        super().update()
        for input_field in self.input_fields:
            input_field.update()
