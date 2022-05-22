import pygame
from codeview.codeblock import *
from codeview.ifblock import IfBlock
from codeview.valueblock import ValueBlock
from codeview.twosidedblock import TwoSidedBlock
class IfElseBlock(IfBlock):
    def __init__(self):
        self.if_false_block = None
        super().__init__()
        
    def build(self):
        super().build()

        #calculate the new height
        self.size.y += CodeBlock.visible_size_y * 2 * self.scale_factor
        if self.if_false_block:
            self.size.y += self.if_false_block.get_chain_size_y()

        #remember the old image
        image = self.image

        #recreate the Surface and its colorkey
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey(INVISIBLE_COLOR)
        self.image.fill(INVISIBLE_COLOR)
        self.rect = self.image.get_rect()

        #redraw left border
        border_width = IfBlock.border_width * self.scale_factor
        overlap = self.circle_radius - self.circle_overlap#overlapping circle(height)
        border_rect = pygame.rect.Rect(0, 0, border_width, self.size.y - overlap)
        pygame.draw.rect(self.image, self.background_color, border_rect)
        pygame.draw.rect(self.image, (0,0,0), border_rect, width=2)

        #draw the normal if-block image to the new one
        self.image.blit(image, (0,0))

        #delete the resulting borders
        rect = delete_rect = pygame.rect.Rect((2, image.get_size()[1] - 2 - CodeBlock.invisible_size_y * self.scale_factor), (border_width - 4, 4))
        pygame.draw.rect(self.image, self.background_color, delete_rect)

        #draw the closing block
        rect = self.code_block_image.get_rect()
        rect.bottomleft = (border_width, self.size.y)
        self.image.blit(self.code_block_image, rect)

        #delete the resulting borders
        rect = pygame.rect.Rect((border_width - 4, self.image.get_size()[1] - rect.height + 2), (8, CodeBlock.visible_size_y * self.scale_factor - 4))
        pygame.draw.rect(self.image, self.background_color, rect)

        #create else-text visualisation
        font = pygame.font.Font(None, int(30 * self.scale_factor))
        else_text = font.render("Else" ,True, (0,0,0))
        else_text_rect = else_text.get_rect()
        else_text_rect.centery = (CodeBlock.visible_size_y * 2.5) *self.scale_factor
        if self.if_true_block:
            else_text_rect.centery += self.if_true_block.get_chain_size_y()
        else_text_rect.left = self.distance_x * self.scale_factor + border_width
        self.image.blit(else_text, else_text_rect)

    def get_min_width(self):
        top_width = super().get_min_width()
        bottom_width = 0
        if self.if_false_block:
            bottom_width = self.if_false_block.get_max_chain_width()

        if top_width > bottom_width:
            return top_width
        else:
            return bottom_width

    def rebuild(self):
        super().rebuild()
        if self.if_false_block:
            self.if_false_block.adjust_to_parent()
            self.if_false_block.adjust_blocks()
    
    def update_scale_factor(self, scalefactor):
        if self.if_false_block:
            self.if_false_block.update_scale_factor(scalefactor)  
        super().update_scale_factor(scalefactor)   
        if self.if_false_block:
            self.if_false_block.adjust_to_parent()

    def try_to_connect(self, block):
        #TODO Problem mit der Reihenfolge kann nucht einfach das vorhermachen. sonst verbindet es in der falschen Reihenfolge
        #Lösung durch aulagerung in Methode?

        #only connect with the ifalse condition block if the given block is a value block
        if isinstance(block, ValueBlock):
            if self.if_false_block:
                appended = self.if_false_block.try_to_connect(block)
                if appended:
                    self.rebuild()
                    return appended
        
        return super().try_to_connect(block)

    def try_to_connect_inside(self, block):
        """Trys to connect with the inside"""
        appended = super().try_to_connect_inside(block)
        if appended:
            return appended
        
        #connect with the condition false blockpart
        if not self.if_false_block:
            #create the Rect for Collision
            pos = pygame.Vector2(IfBlock.border_width * self.scale_factor, CodeBlock.visible_size_y * self.scale_factor * 3)
            if self.if_true_block:
                pos.y += self.if_true_block.get_chain_size_y()
            pos += self.position
            size_rect = (self.get_size().x - IfBlock.border_width * self.scale_factor, CodeBlock.invisible_size_y * self.scale_factor)

            conditional_invisble_rect = pygame.rect.Rect(pos, size_rect)
            if conditional_invisble_rect.colliderect(block.rect):
                self.if_false_block = block
                self.if_false_block.parent_block = self
                self.rebuild()
                return block
        else:#ask the next block in the condition 
            appended = self.if_false_block.try_to_connect(block)
            if appended:
                self.rebuild()
                return appended

        

    def give_keyboard_down_event(self, event):
        super().give_keyboard_down_event(event)
        if self.if_false_block:
            self.if_false_block.give_keyboard_down_event(event)

    def get_collider(self, mouse_position: pygame.Vector2):
        if self.if_false_block:#check collision with blocks in condition false part
                collider = self.if_false_block.get_collider(mouse_position)
                if collider == self.if_false_block:
                    self.if_false_block.parent_block = None
                    self.if_false_block = None
                if collider:
                    self.rebuild()
                    return collider
        return super().get_collider(mouse_position)

    def get_connection_point_bottom(self, child):
        if child == self.if_false_block:
            connection_point = self.get_connection_point_top() 
            #add the height of the header if and else block and the empyt block
            connection_point.y += 3 * CodeBlock.visible_size_y * self.scale_factor

            #add the chain size if the if_false_block
            if self.if_true_block:
                connection_point.y += self.if_true_block.get_chain_size_y()

            return connection_point
        else:
            return super().get_connection_point_bottom(child)

    def move(self, movement: pygame.Vector2):
        super().move(movement)
        if self.if_false_block:
            self.if_false_block.move(movement)

    def update(self):
        super().update()
        if self.if_false_block:
            self.if_false_block.update()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if self.if_false_block:
            self.if_false_block.draw(screen)

