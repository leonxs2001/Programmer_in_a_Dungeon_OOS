import pygame
from codeview.block.codeblock import CodeBlock

class StartBlock(CodeBlock):
    start_position = pygame.Vector2(770,215)
    def __init__(self, background_color = (255,130,0)):
        super().__init__(background_color)
    def build(self):
        super().build()
        font = pygame.font.Font(None, int(50 * self.scale_factor))
        start_text = font.render("Start", True, (0,0,0))
        start_rect = start_text.get_rect()
        start_rect.center = self.get_size() / 2
        self.image.blit(start_text, start_rect)

class InitializationBlock(CodeBlock):
    start_position = pygame.Vector2(210,215)
    def __init__(self, background_color = (130,255,0)):
        super().__init__(background_color)
    def build(self):
        super().build()
        font = pygame.font.Font(None, int(50 * self.scale_factor))
        start_text = font.render("Initialization", True, (0,0,0))
        start_rect = start_text.get_rect()
        start_rect.center = self.get_size() / 2
        self.image.blit(start_text, start_rect)