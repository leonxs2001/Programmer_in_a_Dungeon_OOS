import pygame
from codeview.codeblock import CodeBlock

class StartBlock(CodeBlock):
    id = "start"
    start_position = pygame.Vector2(640,360)
    def __init__(self, background_color=...):
        super().__init__(background_color)