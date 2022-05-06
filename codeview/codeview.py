import pygame
from pygame.locals import *
from fight.bullet import Bullet
from codeview.codeblock import CodeBlock
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
        self.code_block_group = pygame.sprite.Group()
        self.code_block_group.add(CodeBlock())
        
        co = CodeBlock()
        co.position = pygame.Vector2(100,100)
        self.code_block_group.add(co)
    def give_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.is_mouse_button_down = True
            self.last_mouse_position = pygame.mouse.get_pos()
            for code_block in self.code_block_group:
                code_block.mouse_button_down()
        elif event.type == MOUSEBUTTONUP:
            self.is_mouse_button_down = False
            for code_block in self.code_block_group:
                code_block.mouse_button_up()
        elif event.type == MOUSEWHEEL:
            self.scale_factor += event.y/10
            if self.scale_factor < 0.2:
                self.scale_factor = 0.2
            elif self.scale_factor > 4.7:
                self.scale_factor = 4.7
            for code_block in self.code_block_group:
                code_block.update_scale_factor(self.scale_factor)
    def update(self):
        if self.is_mouse_button_down:
            mouse_position = pygame.Vector2(pygame.mouse.get_pos())
            distance = self.last_mouse_position - mouse_position
            self.last_mouse_position = mouse_position
            for code_block in self.code_block_group:
                code_block.position -= distance
        self.code_block_group.update()
    def draw(self, screen):
        screen.fill((255,255,255))
        self.code_block_group.draw(screen)