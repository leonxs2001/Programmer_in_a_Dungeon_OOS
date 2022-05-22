from shutil import move
import pygame
from codeview.block import Block

class InputField:
    empty_size = pygame.Vector2(70,30)
    distance_x = 7
    def __init__(self, left_center = pygame.Vector2(0,0)):
        self.value = 1
        self.scale_factor = 1
        self.left_center = left_center
        self.in_focus = False
        self.cursor_counter = 0 # if %20 < 10 draw and not if > 10
        self.build()
        
    def build(self):
        if not isinstance(self.value, Block):
            self.size = InputField.empty_size * self.scale_factor

            min_length = self.size.x
            distance = InputField.distance_x * self.scale_factor
            font = pygame.font.Font(None, int(25 * self.scale_factor))
            text = font.render(str(self.value),True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.centery = self.size.y / 2
            text_rect.left = distance

            length = distance * 2 + text.get_width()
            if length > min_length:
                self.size.x = length
            
            self.image = pygame.Surface(self.size)
            self.image.fill((255,255,255))
            self.rect = self.image.get_rect()
            pygame.draw.rect(self.image, (0,0,0), pygame.rect.Rect((0,0), self.size), width=2)

            self.image.blit(text, text_rect)

            cursor_pos_x = length -  distance
            cursor_pos_x += self.left_center.x
            self.cursor_rect = pygame.rect.Rect((cursor_pos_x, 0), (distance/2, text.get_height()))
            self.cursor_rect.centery = self.left_center.y
    
    def rebuild(self):
        if isinstance(self.value, Block):
            self.value.rebuild()
        else:
            self.build()

    def get_size(self):
        """Return size with scalefactor"""
        if isinstance(self.value, Block):
            return self.value.get_size()
        else:
            return self.size.copy()

    def get_collider(self, mouseposition: pygame.Vector2):
        """Returns the colliding part in the inputfield"""
        if isinstance(self.value, Block):
            return self.value.get_collider(mouseposition)
        else:
            if self.rect.collidepoint(mouseposition):
                self.in_focus = True

    def try_to_connect(self, block):
        if isinstance(self.value, Block):
            return self.value.try_to_connect(block)
        else:
            if self.rect.colliderect(block.rect):
                self.append(block)
                return block

    def update_scale_factor(self, scalefactor): 
        last_scale_factor = self.scale_factor
        self.scale_factor = scalefactor

        #get the current mouseposition for moving the images in the right way(center of movemet is the mouseposition).
        center_of_scrollment = pygame.mouse.get_pos()
        distance = (self.left_center - center_of_scrollment) / last_scale_factor
        distance *= scalefactor
        self.left_center = center_of_scrollment + distance

        if isinstance(self.value, Block):
            self.value.update_scale_factor(scalefactor)

        #build self
        self.build()

    def adjust_block_to_input_field(self):
        if isinstance(self.value, Block):
            self.value.adjust_to_input_field(self)

    def __str__(self):
        return f"{self.value}"

    def append(self, value_block):
        self.value = value_block
        self.adjust_block_to_input_field()

    def move(self, movement):
        self.left_center += movement
        self.cursor_rect.topleft += movement
        if isinstance(self.value, Block):
            self.value.move(movement)

    def update(self):
        self.rect.left = self.left_center.x
        self.rect.centery = self.left_center.y

        #reset focus if mouse_button is clicked again
        if self.in_focus:
            if pygame.mouse.get_pressed()[0] and not self.rect.collidepoint(pygame.mouse.get_pos()):
                self.in_focus = False 
            else:
                pass#do writing stuff here
        
        if isinstance(self.value, Block):
            self.value.update()

    def draw(self, screen): 
        if isinstance(self.value, Block):
            self.value.draw(screen)
        else:
            screen.blit(self.image, self.rect)
            if self.in_focus:
                self.cursor_counter += 1
                if self.cursor_counter % 40 < 25:
                    pygame.draw.rect(screen, (0,0,0),self.cursor_rect)
