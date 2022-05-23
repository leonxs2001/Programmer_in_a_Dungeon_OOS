import pygame
from pygame.locals import *
from codeview.selector import Selector
from codeview.block import Block
from codeview.startblock import *
from level import Level
class CodeView(Level):
    def __init__(self):
        super().__init__()
        self.selector = Selector()
        self.scale_factor = 1

        self.is_mouse_button_down = False
        self.last_mouse_position = pygame.Vector2(0,0)

        self.code_block_list = [StartBlock(), InitializationBlock()]
        
    def give_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                selector_collision = self.selector.check_collision(pygame.Vector2(mouse_position))
                if selector_collision:
                    if isinstance(selector_collision, Block):#add to the block list
                        
                        selector_collision.in_focus = True
                        self.is_mouse_button_down = True
                        self.last_mouse_position = mouse_position#reset last mouseposition
                        selector_collision.update_scale_factor(self.scale_factor)
                        pos = mouse_position - selector_collision.get_size() / 2
                        selector_collision.move(pos - selector_collision.position)
            
                        self.code_block_list.append(selector_collision)
                else:
                    #save, that mousebutton is pressed and the current mouse position
                    self.is_mouse_button_down = True
                    self.last_mouse_position = pygame.mouse.get_pos()  

                    #check mousecollison with blocks 

                    for code_block in self.code_block_list[::-1]:#backwards because we want to grab the one we see
                        #get colliding block or a None
                        collider = code_block.get_collider(self.last_mouse_position)
                        if collider and isinstance(collider, Block):
                            #add colliding block to blocklist(first save in another list to avoid an endless loop) if its not the focused block
                            if collider == code_block:
                                self.code_block_list.remove(collider)#remove the element, for putting it later to the end
                            self.code_block_list.append(collider)
                            break

        elif event.type == MOUSEBUTTONUP:
            if not pygame.mouse.get_pressed()[0]:
                #check for new possible connections
                for code_block1 in self.code_block_list:
                    if code_block1.in_focus:
                        for code_block2 in self.code_block_list[::-1]:#backwards because the last one is the one we see
                            if code_block1 != code_block2:
                                #try to connect the focused block with every else
                                appended_block = code_block2.try_to_connect(code_block1)
                                #remove the block from block list if existing
                                if appended_block and appended_block in self.code_block_list:
                                    self.code_block_list.remove(appended_block)
                                    break#only connect two blocks with each other
                #reset the information
                self.is_mouse_button_down = False
                #tell every block, that mouse button 
                for code_block in self.code_block_list:
                    code_block.mouse_button_up()

        elif event.type == KEYDOWN:#give the key down event to the blocks
            for code_block in self.code_block_list:
                code_block.give_keyboard_down_event(event)
        elif event.type == MOUSEWHEEL:
            if not self.selector.scroll(event.y):
                #update scalefactor in borders from 0.4 to 3.5 
                self.scale_factor += event.y/10
                if self.scale_factor < 0.4:
                    self.scale_factor = 0.4
                elif self.scale_factor > 3.5:
                    self.scale_factor = 3.5
                #give new scalefactor to the blocks
                for code_block in self.code_block_list:
                    code_block.update_scale_factor(self.scale_factor)

    def update(self):
        #proccess the viewmovement if mousebutton is pressed
        if self.is_mouse_button_down:
            #calculate mousemovement from the last update to now
            mouse_position = pygame.Vector2(pygame.mouse.get_pos())
            movement = mouse_position - self.last_mouse_position
            self.last_mouse_position = mouse_position
            
            #move the block in focus or notice, that the mouse is not on a block
            is_on_code_block = False
            for code_block in self.code_block_list:
                if code_block.in_focus:
                    is_on_code_block = True
                    code_block.move(movement)
                    break
            
            #move every block if the mouse is not on a block
            if not is_on_code_block:
                for code_block in self.code_block_list:
                    code_block.move(movement)

        #update every block
        for code_block in self.code_block_list:
            code_block.update()

    def draw(self, screen):
        #draw background
        screen.fill((255,255,255))
        for code_block in self.code_block_list:
            code_block.draw(screen)
        self.selector.draw(screen)