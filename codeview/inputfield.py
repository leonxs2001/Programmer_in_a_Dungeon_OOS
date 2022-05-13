from turtle import update
import pygame

class InputField:
    empty_size = pygame.Vector2(70,30)
    def __init__(self, left_center):
        self.value = None
        self.scale_factor = 1
        self.build()
        self.left_center = left_center
        
    def build(self):
        if not self.value:
            size = InputField.empty_size * self.scale_factor
            self.image = pygame.Surface(size)
            self.image.fill((255,255,255))
            self.rect = self.image.get_rect()
            pygame.draw.rect(self.image, (0,0,0), pygame.rect.Rect((0,0), size), width=2)
    
    def rebuild(self):
        if self.value:
            self.value.rebuild()
        else:
            self.build()

    def get_size(self):
        """Return size with scalefactor"""
        if self.value:
            return self.value.get_size()
        else:
            return InputField.empty_size * self.scale_factor

    def get_collider(self, mouseposition: pygame.Vector2):
        """Returns the colliding part in the inputfield"""
        if self.value:
            return self.value.get_collider(mouseposition)

    def try_to_connect(self, block):
        if self.value:
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

        if self.value:
            self.value.update_scale_factor(scalefactor)

        #build self
        self.build()

    def adjust_block_to_input_field(self):
        if self.value:
            self.value.adjust_to_input_field(self)

    def __str__(self):
        return f"{self.value}"

    def append(self, value_block):
        self.value = value_block
        self.adjust_block_to_input_field()

    def move(self, movement):
        self.left_center += movement
        if self.value:
            self.value.move(movement)

    def update(self):
        self.rect.left = self.left_center.x
        self.rect.centery = self.left_center.y
        if self.value:
            self.value.update()

    def draw(self, screen): 
        if self.value:
            self.value.draw(screen)
        else:
            screen.blit(self.image, self.rect)
