import pygame
class Block:
    """Abstract Class"""
    start_position = pygame.Vector2(10,10)
    def __init__(self, background_color = (130,130,130)):
        self.background_color = background_color
        self.scale_factor = 1
        self.position = self.start_position.copy()

        self.in_focus = False

        self.build()

    def update_scale_factor(self, scalefactor):
        last_scale_factor = self.scale_factor
        self.scale_factor = scalefactor

        #get the current mouseposition for moving the images in the right way(center of movemet is the mouseposition).
        center_of_scrollment = pygame.mouse.get_pos()
        distance = (self.position - center_of_scrollment) / last_scale_factor
        distance *= scalefactor
        self.position = center_of_scrollment + distance

        #rebuild the image with the new scalefactor and size
        self.build()

    def build(self):
        """Overwrite and create the self.image Surface for the block."""
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
    
    def get_collider(self, mouse_position : pygame.Vector2):
        """Return the colliding Block and delete from the current structure"""
        if self.rect.collidepoint(mouse_position):
            self.in_focus = True
            return self
    def try_to_connect(self, block):
        """Try to connect with the given block"""
        pass
    def mouse_button_up(self):
        """Reset the focus"""
        self.in_focus = False

    def move(self, movement : pygame.Vector2):
        self.position += movement
    
    def update(self):
        self.rect.topleft = self.position

    def draw(self, screen : pygame.Surface):
        screen.blit(self.image, self.rect)