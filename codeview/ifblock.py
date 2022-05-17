import pygame
from codeview.codeblock import *
from codeview.twosidedblock import TwoSidedBlock
class IfBlock(TwoSidedBlock):
    start_position = pygame.Vector2(100,100)
    def build(self):
        super().build()
        image = self.image #copy image from normal build
        rect = image.get_rect()

        #create Surface
        border_width = 0.1 * super().get_size().x # is border the right name????
        overlap = self.circle_radius - self.circle_overlap#overlapping circle(height)
        size = pygame.Vector2(super().get_size().x + border_width, CodeBlock.visible_size_y * self.scale_factor * 3 + overlap)
        self.image = pygame.transform.scale(self.image, size)
        self.image.fill(INVISIBLE_COLOR)
        self.rect = self.image.get_rect()
        #draw the normal block image to the new one
        rect.topright = (size.x, 0)
        self.image.blit(image, rect)

        #draw left border
        border_rect = pygame.rect.Rect(0,0,border_width, size.y - overlap)
        pygame.draw.rect(self.image, self.background_color, border_rect)
        pygame.draw.rect(self.image, (0,0,0), border_rect, width=2)

        #delete the resulting borders
        pygame.draw.rect(self.image, self.background_color, pygame.rect.Rect((border_width - 2, 2), (4, CodeBlock.visible_size_y * self.scale_factor - 4)))

        #draw the closing block
        rect.top = size.y - self.visible_size_y * self.scale_factor - overlap
        self.image.blit(image,rect)

        #delete the resulting borders
        pygame.draw.rect(self.image, self.background_color, pygame.rect.Rect((border_width - 2, 2 + rect.top), (4, CodeBlock.visible_size_y * self.scale_factor - 4)))
        