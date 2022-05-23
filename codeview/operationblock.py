import pygame
from codeview.valueblock import ValueBlock
class OperationBlock(ValueBlock):
    def __init__(self, operation = "+", number_of_operators = 2):
        if number_of_operators == 1:
            super().__init__(operation, operation, ("",))
        else:
            params = [operation for i in range(1,number_of_operators)]
            params = ["",] + params
            super().__init__("", operation, params)
    def render_text(self, text):
        font = pygame.font.Font(None, int(25 * self.scale_factor))
        return font.render(text ,True, (0,0,0)) 