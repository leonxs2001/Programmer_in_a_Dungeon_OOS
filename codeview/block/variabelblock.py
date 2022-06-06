from unittest import result
import pygame
from codeview.block.valueblock import ValueBlock
from codeview.block.methodblock import MethodBlock
class VariabelBlock(ValueBlock):
    def __init__(self, name="var"):
        super().__init__(name, name, parameters=())
    def get_code_string(self):
        return f"${self.representation}"

class VariabelDefinitionBlock(MethodBlock):
    def __init__(self, variabel_name):
        super().__init__("", variabel_name, parameters=(variabel_name+" = ",))
    
    def render_text(self, text):
        font = pygame.font.Font(None, int(25 * self.scale_factor))
        return font.render(text, True, (0,0,0)) 

    def get_code_string(self):
        result = f"${self.representation}={self.input_fields[0].get_code_string()}" 
        if self.next_block:
            result += self.next_block.get_code_string()
        
        return result