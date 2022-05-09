import pygame
from codeview.codeblock import CodeBlock

class StartBlock(CodeBlock):
    id = "start"
    def __init__(self, background_color=...):
        super().__init__(background_color)