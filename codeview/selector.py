import copy
import pygame
from codeview.block.blockcreation import block_dict
class Selector:
    arrow_size = pygame.Vector2(20,40)
    background_color = (220,220,220)
    def __init__(self):
        self.open = False
        self.build()

    def build(self):
        #create the little arrow image
        self.arrow_image = pygame.Surface(Selector.arrow_size)
        self.arrow_image.fill(Selector.background_color)
        pygame.draw.rect(self.arrow_image, (0,0,0), pygame.rect.Rect((0,0), Selector.arrow_size),width=2)
        center_y = Selector.arrow_size.y / 2
        pygame.draw.lines(self.arrow_image, (0,0,0), False, [(0,0), (Selector.arrow_size.x, center_y), (0, Selector.arrow_size.y)], width=3)
        self.arrow_image_rect = self.arrow_image.get_rect()
        self.arrow_image_rect.centery = 360

        self.drawn_arrow_image = self.arrow_image.copy()

        #create backgroundsuface
        self.background_image = pygame.Surface((400, 720))
        self.background_image.fill(Selector.background_color)
        pygame.draw.rect(self.background_image, (0,0,0), pygame.rect.Rect((0,0), (400, 720)),width=2)

        #get all possible blocks
        self.blocks = []
        x = 10
        y = 10
    
        for tup in block_dict:
            block = block_dict[tup]
            rect = block.image.get_rect()
            rect.topleft = (x, y)
            y += 10 + block.image.get_height()
            self.blocks.append((block.image, rect, tup))

    def scroll(self, scrollment):
        if self.open and pygame.mouse.get_pos()[0] < 400:
            #check if the scrollment stays in the right frame
            scrollment = scrollment * 12
            first_y = self.blocks[0][1].top 
            next_first_y = first_y + scrollment
     
            if next_first_y > 10:
                scrollment = 10 - first_y
            else:
                last_y = self.blocks[-1][1].bottom
                next_last_y = last_y + scrollment 
                if next_last_y < 710:
                    scrollment = (710 - last_y)

            #update every block with scrollment
            for block in self.blocks:
                block[1].top += scrollment
            return True
        else:
            return False

    def check_collision(self, mouse_position : pygame.Vector2):
        if self.arrow_image_rect.collidepoint(mouse_position):
            self.open = not self.open
            if self.open:
                self.arrow_image_rect.left = 400 -1
                self.drawn_arrow_image = pygame.transform.rotate(self.arrow_image, 180)
            else:
               self.arrow_image_rect.left = 0
               self.drawn_arrow_image = self.arrow_image.copy()
            return True
        else:
            if self.open and mouse_position.x < 400:
                #check collision with all rects
                for block in self.blocks:
                    if block[1].collidepoint(mouse_position):
                        self.open = False
                        self.arrow_image_rect.left = 0
                        return copy.copy(block_dict[block[2]])
                    
                return True
            return False 

    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.drawn_arrow_image, self.arrow_image_rect)
        if self.open:#only draw background if its open
            screen.blit(self.background_image, (0,0))
        
            for block_tupel in self.blocks:
                screen.blit(block_tupel[0],block_tupel[1])