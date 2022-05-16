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

    def adjust_to_parent(self):
        """Adjust self to the given parent block"""
        if self.parent_block:
            half_size_difference_x = (self.visible_size.x - self.parent_block.visible_size.x)/2
            self.position = self.parent_block.position + (-half_size_difference_x, self.parent_block.visible_size.y - 1)

    def clear_next_block(self):
        self.next_block.parent_block = None
        super().clear_next_block()