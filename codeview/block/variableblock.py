import pygame
from codeview.block.valueblock import ValueBlock
from codeview.block.methodblock import MethodBlock
class VariableBlock(ValueBlock):
    def __init__(self, name="var"):
        super().__init__(name, name, parameters=())
class VariableDefinitionBlock(MethodBlock):
    def __init__(self, variable_name):
        super().__init__("", variable_name, parameters=(variable_name+" = ",))
    
    def render_text(self, text):
        font = pygame.font.Font(None, int(25 * self.scale_factor))
        return font.render(text, True, (0,0,0)) 