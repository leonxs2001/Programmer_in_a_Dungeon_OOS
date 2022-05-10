import pygame

class InputField:
    def __init__(self, left_center):
        self.size = pygame.Vector2(70,25)
        self.build(self.size)
        self.left_center = left_center
        self.scale_factor = 1

    def build(self, size):
        self.image = pygame.Surface(size)
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (0,0,0), pygame.rect.Rect((0,0), size), width=2)

    def update_scale_factor(self, scalefactor): 
        last_scale_factor = self.scale_factor
        self.scale_factor = scalefactor

        self.build(self.size * scalefactor)
        center_of_scrollment = pygame.mouse.get_pos()
        distance = (self.left_center - center_of_scrollment) / last_scale_factor
        distance *= scalefactor
        self.left_center = center_of_scrollment + distance

    def move(self, movement):
        self.left_center += movement

    def update(self):
        self.rect.left = self.left_center.x
        self.rect.centery = self.left_center.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
