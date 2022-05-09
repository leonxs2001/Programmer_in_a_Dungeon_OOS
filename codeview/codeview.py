from tabnanny import check
import pygame
from pygame.locals import *
from codeview.codeblock import CodeBlock
from codeview.startblock import StartBlock
from codeview.methodblock import MethodBlock
from level import Level
class CodeView(Level):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.scale_factor = 1
        self.last_mouse_position = pygame.Vector2(0,0)
        self.is_mouse_button_down = False
        start = StartBlock((255,130,0))
        bla = MethodBlock()
        bla.append(MethodBlock())
        start.position = pygame.Vector2(600,400)
        start.append(MethodBlock())
        start.append(MethodBlock())
        start.append(MethodBlock())
        start.append(MethodBlock())
        start.append(bla)
        self.code_block_list = [start, MethodBlock(parameters=("x","y"))]
        
    def give_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.is_mouse_button_down = True
            self.last_mouse_position = pygame.mouse.get_pos()  
            #check collison with blocks 
            new_blocks = []
            for code_block in self.code_block_list:
                collider = code_block.get_collider(self.last_mouse_position)
                if collider:
                    if collider != code_block:
                        new_blocks.append(collider)
                    break    
            self.code_block_list += new_blocks

        elif event.type == MOUSEBUTTONUP:
            #check for new connections
            for code_block1 in self.code_block_list:
                if code_block1.in_focus:
                    for code_block2 in self.code_block_list:
                        if code_block1 != code_block2:
                            appended_block = code_block1.try_to_connect(code_block2)
                            if appended_block:
                                self.code_block_list.remove(appended_block)
            self.is_mouse_button_down = False
            for code_block in self.code_block_list:
                code_block.mouse_button_up()

        elif event.type == MOUSEWHEEL:
            self.scale_factor += event.y/10
            if self.scale_factor < 0.4:
                self.scale_factor = 0.4
            elif self.scale_factor > 3.5:
                self.scale_factor = 3.5
            for code_block in self.code_block_list:
                code_block.update_scale_factor(self.scale_factor)

    def update(self):
        if self.is_mouse_button_down:
            mouse_position = pygame.Vector2(pygame.mouse.get_pos())
            movement = mouse_position - self.last_mouse_position
            self.last_mouse_position = mouse_position
            is_on_code_block = False
            for code_block in self.code_block_list:
                if code_block.in_focus:
                    is_on_code_block = True
                    code_block.move(movement)
                    break

            if not is_on_code_block:
                for code_block in self.code_block_list:
                    code_block.move(movement)

        for code_block in self.code_block_list:
            code_block.update()

    def draw(self, screen):
        screen.fill((255,255,255))
        for code_block in self.code_block_list:
            code_block.draw(screen)