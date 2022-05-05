import pygame
from level import Level
class CodeView(Level):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
    def draw(self, screen):
        screen.fill((255,255,255))
        screen.blit(self.image,self.rect)