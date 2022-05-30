import copy
import pygame
from codeview.block.variabelblock import *
from codeview.textinput import TextInput
class Selector:
    arrow_size = pygame.Vector2(20,40)
    background_color = (220,220,220)
    def __init__(self, block_dict):
        self.block_dict = block_dict
        self.open = False
        self.build()
        self.wait_for_input = False
        self.variabels = []

    def reset(self):
        self.arrow_image_rect.left = 0
        self.drawn_arrow_image = self.arrow_image.copy()
        self.open = False
        self.build()

    def build(self):
        self.text_input = TextInput("Your Variabelname:")
        #create the little arrow image
        self.arrow_image = pygame.Surface(Selector.arrow_size)
        self.arrow_image.fill(Selector.background_color)
        self.arrow_image_rect = self.arrow_image.get_rect()
        pygame.draw.rect(self.arrow_image, (0,0,0), self.arrow_image_rect, width=2)
        center_y = Selector.arrow_size.y / 2
        pygame.draw.lines(self.arrow_image, (0,0,0), False, [(0,0), (Selector.arrow_size.x, center_y), (0, Selector.arrow_size.y)], width=3)
        self.arrow_image_rect.centery = 360

        self.drawn_arrow_image = self.arrow_image.copy()

        #create backgroundsurface
        self.background_image = pygame.Surface((400, 720))
        self.background_image.fill(Selector.background_color)
        pygame.draw.rect(self.background_image, (0,0,0), pygame.rect.Rect((0,0), (400, 720)),width=2)

        #create add variabel image
        size = pygame.Vector2(200,60)
        self.add_variabel_image = pygame.Surface(size)
        self.add_variabel_image.fill((230,230,230))
        self.add_variabel_rect = self.add_variabel_image.get_rect()
        pygame.draw.rect(self.add_variabel_image, (0,0,0),  self.add_variabel_rect, width=2)
        font = pygame.font.Font(None, 30)
        btn_text = font.render("Create Variabel", True, (0,0,0))
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = size / 2
        self.add_variabel_image.blit(btn_text, btn_text_rect)

        self.add_variabel_rect.topleft = (10,10)

        #get all possible blocks
        self.blocks = []
        x = 10
        y = 20 + size.y
    
        for tup in list(self.block_dict)[::-1]:
            block = self.block_dict[tup]
            rect = block.image.get_rect()
            rect.topleft = (x, y)
            y += 10 + block.image.get_height()
            self.blocks.append((block.image, rect, tup))

    def scroll(self, scrollment):
        if self.open and pygame.mouse.get_pos()[0] < 400:
            #check if the scrollment stays in the right frame
            scrollment = scrollment * 20
            first_y = self.blocks[0][1].top 
            next_first_y = first_y + scrollment
     
            if next_first_y > 20 + self.add_variabel_rect.height:
                scrollment = 20 + self.add_variabel_rect.height - first_y
            else:
                last_y = self.blocks[-1][1].bottom
                next_last_y = last_y + scrollment 
                if next_last_y < 710:
                    scrollment = (710 - last_y)

            #update every block with scrollment
            for block in self.blocks:
                block[1].top += scrollment

            self.add_variabel_rect.top += scrollment
            return True
        else:
            return False
    def give_keyboard_down_event(self, event):
        if self.wait_for_input:
            self.text_input.give_keyboard_down_event(event)

    def create_new_variabel(self, name):
        variabel_definition_block = VariabelDefinitionBlock(name)
        #add variabel definition block to the dict
        tup = (name, "variabeldefinition")
        self.block_dict[tup] = variabel_definition_block
        tup = (name, "variabel")
        self.block_dict[tup] = VariabelBlock(name)
        self.build()
        
        return variabel_definition_block
    def check_collision(self, mouse_position : pygame.Vector2):
        if self.wait_for_input:
            result = self.text_input.check_collision(mouse_position)
            if result:#got an input
                if isinstance(result, str):
                    if result not in self.variabels:
                        self.wait_for_input = False
                        return self.create_new_variabel(result)
                self.wait_for_input = False
            return True
        else:
            if self.arrow_image_rect.collidepoint(mouse_position):
                self.open = not self.open
                if self.open:
                    self.arrow_image_rect.left = 400 - 1
                    self.drawn_arrow_image = pygame.transform.rotate(self.arrow_image, 180)
                else:
                    self.arrow_image_rect.left = 0
                    self.drawn_arrow_image = self.arrow_image.copy()
                    return True
            else:
                if self.open and mouse_position.x < 400:
                    #check collision with create new variabel button
                    if self.add_variabel_rect.collidepoint(mouse_position):
                        self.open = False
                        self.arrow_image_rect.left = 0
                        self.wait_for_input = True
                        return True
                    #check collision with all rects
                    for block in self.blocks:
                        if block[1].collidepoint(mouse_position):
                            self.open = False
                            self.arrow_image_rect.left = 0
                            return copy.copy(self.block_dict[block[2]])
                        
                    return True
                return False 

    def update(self):
        if self.wait_for_input:
            self.text_input.update()
    
    def draw(self, screen):
        screen.blit(self.drawn_arrow_image, self.arrow_image_rect)
        if self.open:#only draw background if its open
            screen.blit(self.background_image, (0,0))

            screen.blit(self.add_variabel_image, self.add_variabel_rect)

            #draw blocks
            for block_tupel in self.blocks:
                screen.blit(block_tupel[0],block_tupel[1])
        if self.wait_for_input:
            self.text_input.draw(screen)