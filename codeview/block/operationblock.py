import pygame
from codeview.block.valueblock import ValueBlock


class OperationBlock(ValueBlock):
    def __init__(self, operation="+", number_of_operators=2):
        if number_of_operators == 1:
            super().__init__(operation, operation, ("",))
        else:
            params = [operation for i in range(1, number_of_operators)]
            params = ["", ] + params
            super().__init__("", operation, params)

    def render_text(self, text):
        font = pygame.font.Font(None, int(25 * self.scale_factor))
        return font.render(text, True, (0, 0, 0))

    def update(self):
        super().update()

    def get_code_string(self):
        operation = self.representation
        if operation == "and":
            operation = "&"
        elif operation == "or":
            operation = "|"
        elif operation == "not":
            return f"!({self.input_fields[0].get_code_string()})"
        result = "("
        result += self.input_fields[0].get_code_string()  # add first operand
        # add ther other operand and the operator
        for input_field in self.input_fields[1:]:
            result += operation + input_field.get_code_string()
        result += ")"
        return result
