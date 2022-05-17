from shutil import move
from pygame import Vector2
from codeview.codeblock import *
class TwoSidedBlock(CodeBlock):
    def __init__(self):
        self.parent_block = None
        super().__init__()

    def build(self):
        super().build()
        #add/draw the top circle with border(makes this block connectable on both sides)
        pygame.draw.circle(self.image, INVISIBLE_COLOR, (self.circle_x ,-self.circle_overlap), self.circle_radius)
        pygame.draw.circle(self.image, (0,0,0), (self.circle_x ,-self.circle_overlap), self.circle_radius, width = 2)

    def get_connection_point_top(self):
        return self.position + (self.get_size().x / 2, 0)

    def adjust_to_parent(self):
        """Adjust self to the given parent block"""
        if self.parent_block:
            movement = self.parent_block.get_connection_point_bottom(self) - self.get_connection_point_top()
            self.move(movement)

    def clear_next_block(self):
        self.next_block.parent_block = None
        super().clear_next_block()