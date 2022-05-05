import pygame
from codeview.codeblock import codeBlock
from level import Level
class CodeView(Level):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.codeblock = codeBlock()
    def give_event(self, event):
        pass
    def update(self):
        pass
    def draw(self, screen):
        screen.fill((255,255,255))
        self.codeblock.draw(screen)