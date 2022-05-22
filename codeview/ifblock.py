import pygame
from codeview.inputfield import InputField
from codeview.valueblock import ValueBlock
from codeview.codeblock import *
from codeview.twosidedblock import TwoSidedBlock
class IfBlock(TwoSidedBlock):
    start_position = pygame.Vector2(100,100)
    border_width = 30# is border the right name?????????????????????????????
    distance_x = 7
    def __init__(self):
        self.input_field = InputField()
        self.if_true_block = None

        super().__init__()
        

    def build(self):
        #create at first a normal Codeblock with the right size
        #blit it later on the Surface

        border_width = IfBlock.border_width * self.scale_factor
        #create the Visualisation of the classic block(if text with inputfield)
        self.size = pygame.Vector2(0, CodeBlock.size.y * self.scale_factor)
        distance = IfBlock.distance_x * self.scale_factor

        #create if-text visualisation
        font = pygame.font.Font(None, int(30 * self.scale_factor))
        if_text = font.render("If" ,True, (0,0,0))
        if_text_rect = if_text.get_rect()
        center_y = (CodeBlock.visible_size_y * self.scale_factor) / 2
        if_text_rect.centery = center_y
        if_text_rect.left = distance

        self.size.x = distance * 2 + if_text.get_width()
        
        self.input_field.left_center = pygame.Vector2(self.size.x + border_width, center_y) + self.position#reset the position of the input field
        self.size.x += self.input_field.get_size().x + distance
        self.input_field.rebuild()#rebuild the inputfield(cursor movement)

        min_size_x = self.get_min_width()

        if self.size.x < min_size_x:#width should be min CodeBlock.size.x
            self.size.x = min_size_x

        super().build()

        self.code_block_image  = self.image.copy()
        image = self.image #copy image from normal build
        image.blit(if_text, if_text_rect)
        rect = image.get_rect()

        #create Surface values
        overlap = self.circle_radius - self.circle_overlap#overlapping circle(height)
        min_y = CodeBlock.visible_size_y * self.scale_factor * 3 + overlap
        self.size = pygame.Vector2(self.size.x + border_width, min_y)
        if self.if_true_block:# add y size of the elements
            self.size.y += self.if_true_block.get_chain_size_y()
        
        #recreate the Surface and its colorkey
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey(INVISIBLE_COLOR)
        self.image.fill(INVISIBLE_COLOR)
        self.rect = self.image.get_rect()

        #draw the normal block image to the new one
        rect.topright = (self.size.x, 0)
        self.image.blit(image, rect)

        #draw left border
        border_rect = pygame.rect.Rect(0,0, border_width, self.size.y - overlap)
        pygame.draw.rect(self.image, self.background_color, border_rect)
        pygame.draw.rect(self.image, (0,0,0), border_rect, width=2)

        #delete the resulting borders
        pygame.draw.rect(self.image, self.background_color, pygame.rect.Rect((border_width - 4, 2), (8, CodeBlock.visible_size_y * self.scale_factor - 4)))

        #draw the closing block
        rect.top = self.size.y - self.visible_size_y * self.scale_factor - overlap
        self.image.blit(self.code_block_image, rect)

        #delete the resulting borders
        pygame.draw.rect(self.image, self.background_color, pygame.rect.Rect((border_width - 2, 2 + rect.top), (4, CodeBlock.visible_size_y * self.scale_factor - 4)))
    
    def get_size(self):
        return self.size.copy()

    def get_min_width(self):
        """Returns the minimum width of the conditionblock"""
        min_size_x = CodeBlock.size.x * self.scale_factor
        if self.if_true_block:
            min_size_x = self.if_true_block.get_max_chain_width()
        return min_size_x

    def get_chain_size_y(self):
        """returns the size of all blocks together"""
        own_size_y = self.size.y - CodeBlock.invisible_size_y * self.scale_factor #is not the size of the Surface(invisble part on the end)
        if self.next_block:
            return own_size_y + self.next_block.get_chain_size_y()
        else:
            return own_size_y

    def get_connection_point_top(self):
        border_width = IfBlock.border_width * self.scale_factor
        new_width = self.get_size().x - border_width
        return pygame.Vector2(new_width / 2 + border_width, 0) + self.position

    def get_connection_point_bottom(self, child):
        """Returns the connection point dependent on which child is given"""
        if child == self.next_block:
            return self.get_connection_point_top() + (0, self.size.y - CodeBlock.invisible_size_y * self.scale_factor )
        else:
            if child == self.if_true_block:
                return self.get_connection_point_top() + (0, CodeBlock.visible_size_y * self.scale_factor)
        return  super().get_connection_point_bottom()

    def get_last_invisible_rect(self):
        """Returns the invisible rect of the last element in the line(bottom)"""
        if self.next_block: #if this block has one next_block pass it on to it
            return self.next_block.get_last_invisible_rect()
        else:
            #create the invisible rect 
            invisible_size = pygame.Vector2(self.get_size().x, CodeBlock.invisible_size_y * self.scale_factor)
            invisible_position = self.position + (0, self.size.y - invisible_size.y)
            invisible_rect = pygame.rect.Rect(invisible_position, invisible_size)
            return invisible_rect

    def rebuild(self):
        """Rebuild self and all input_fields"""
        self.input_field.rebuild()
        self.build()
        self.adjust_to_parent()
        self.adjust_blocks()
        if self.if_true_block:
            self.if_true_block.adjust_to_parent()
            self.if_true_block.adjust_blocks()

    def adjust_to_parent(self):
        #track the current position adjust to parent and give the movement to the inputfield
        position = self.position
        super().adjust_to_parent()
        movement = self.position - position
        self.input_field.move(movement)

    def update_scale_factor(self, scalefactor):
        self.input_field.update_scale_factor(scalefactor)
        if self.if_true_block:
            self.if_true_block.update_scale_factor(scalefactor)  
        super().update_scale_factor(scalefactor)   
        if self.if_true_block:
            self.if_true_block.adjust_to_parent()

    def give_keyboard_down_event(self, event):
        super().give_keyboard_down_event(event)
        self.input_field.give_keyboard_down_event(event)
        if self.if_true_block:
            self.if_true_block.give_keyboard_down_event(event)

    def try_to_connect(self, block):
        #only connect with the input field or the condition block if the given block is a value block
        if isinstance(block, ValueBlock):
            appended = self.input_field.try_to_connect(block)
            if appended:
                self.rebuild()
                return appended
            if self.if_true_block:
                appended = self.if_true_block.try_to_connect(block)
                if appended:
                    self.rebuild()
                    return appended

        #connect with the condition blockpart
        if isinstance(block, TwoSidedBlock):
            if not self.if_true_block:
                #create the Rect for Collision
                pos = (IfBlock.border_width * self.scale_factor, CodeBlock.visible_size_y * self.scale_factor)
                pos += self.position
                size_rect = (self.get_size().x - IfBlock.border_width * self.scale_factor, CodeBlock.invisible_size_y * self.scale_factor)

                conditional_invisble_rect = pygame.rect.Rect(pos, size_rect)
                if conditional_invisble_rect.colliderect(block.rect):
                    self.if_true_block = block
                    self.if_true_block.parent_block = self
                    self.rebuild()
                    return block
            else:#ask the next block in the condition 
                appended = self.if_true_block.try_to_connect(block)
                if appended:
                    self.rebuild()
                    return appended
        
        return super().try_to_connect(block)

    def get_collider(self, mouse_position: pygame.Vector2):
        #check the collision with the input field
        collider = self.input_field.get_collider(mouse_position)
        if collider:
            if collider == self.input_field.value:
                self.input_field.value = "1"
                self.input_field.rebuild()
            collider.rebuild()
            self.rebuild()
            return collider
        else:
            if self.if_true_block:#check collision with blocks in condition part
                collider = self.if_true_block.get_collider(mouse_position)
                if collider == self.if_true_block:
                    self.if_true_block.parent_block = None
                    self.if_true_block = None
                if collider:
                    self.rebuild()
                    return collider

        return super().get_collider(mouse_position)

    def move(self, movement: pygame.Vector2):
        super().move(movement)
        self.input_field.move(movement)
        if self.if_true_block:
            self.if_true_block.move(movement)

    def update(self):
        super().update()
        self.input_field.update()
        if self.if_true_block:
            self.if_true_block.update()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        self.input_field.draw(screen)
        if self.if_true_block:
            self.if_true_block.draw(screen)
        