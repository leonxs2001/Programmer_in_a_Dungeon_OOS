from tabnanny import check
import pygame
from pygame.locals import *
from codeview.block import Block
from codeview.operationblock import OperationBlock
from codeview.variableblock import VariableBlock
from codeview.ifelseblock import IfElseBlock
from codeview.valueblock import ValueBlock
from codeview.ifblock import IfBlock
from codeview.startblock import StartBlock
from codeview.methodblock import MethodBlock
from level import Level
class CodeView(Level):
    def __init__(self):
        super().__init__()

        self.scale_factor = 1

        self.is_mouse_button_down = False
        self.last_mouse_position = pygame.Vector2(0,0)

        start = StartBlock((255,130,0))
        bla = MethodBlock()
        bla.append(MethodBlock())
        start.position = pygame.Vector2(600,400)
        start.append(MethodBlock())
        start.append(MethodBlock())
        start.append(MethodBlock())
        start.append(MethodBlock())
        start.append(MethodBlock(parameters=("number",), name="count"))
        start.append(bla)
        
        #list of (start)blocks.
        #MethodBlock(parameters=("x","y"))
        self.code_block_list = [start,MethodBlock(parameters=("x","y")), ValueBlock(parameters=("A1", "A2"), name="A"),ValueBlock(parameters=("B1", "B2"), name="B"),ValueBlock(name = "lajsdflkjasdhlkj", parameters=()), IfBlock(), IfElseBlock(), OperationBlock(), VariableBlock("test") ]
        
    def give_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
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