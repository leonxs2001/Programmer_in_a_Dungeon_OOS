import pygame
from pygame.locals import *
from codeview.stringtocode import get_blocks_from_string
from selectioninput import SelectionInput
from sqlitedataaccess import SqliteDataAccess
from codeview.textinput import TextInput
from codeview.block.variabelblock import VariabelDefinitionBlock
from codeview.menu import Menu
from codeview.selector import Selector
from codeview.block.block import Block
from codeview.block.startblock import *
from codeview.block.blockcreation import block_dict
from level import Level
class CodeView(Level):
    def __init__(self):
        super().__init__()
        self.selector = Selector(block_dict)
        self.scale_factor = 1

        self.is_mouse_button_down = False
        self.last_mouse_position = pygame.Vector2(0,0)
        self.menu = Menu()

        self.code_block_list = [StartBlock(), InitializationBlock()]
        self.wait_for_input = False
        self.wait_for_selection = False

        self.text_input = TextInput("Name your Code:")
        self.selection_input = SelectionInput("Choose your code:")

        self.data_accessor = SqliteDataAccess()

    def reset(self):
        #delete old variabels
        erasable = []
        for tup in block_dict:
            if tup[1] == "variabel" or tup[1] == "variabeldefinition":
                erasable.append(tup)
        for e_tup in erasable:
            del block_dict[e_tup]
            self.scale_factor = 1
        
        self.code_block_list = [StartBlock(), InitializationBlock()]
        self.selector.reset()

    def give_event(self, event):
        if self.wait_for_input:
            if event.type == KEYDOWN:
                self.text_input.give_keyboard_down_event(event)
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    result = self.text_input.check_collision(pygame.mouse.get_pos())
                    if result:
                        if isinstance(result, str):
                            self.wait_for_input = False
                            code = ""
                            initialization_code = ""
                        
                            for block in self.code_block_list:
                                if isinstance(block, StartBlock):
                                    code = block.get_code_string()
                                elif isinstance(block, InitializationBlock):
                                    initialization_code = block.get_code_string()
                            self.data_accessor.save_item(result, code, initialization_code, opponent=True)
                            return True
                        else:
                            self.wait_for_input = False
        elif self.wait_for_selection:#wait for loading selection
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    result = self.selection_input.check_collision(pygame.mouse.get_pos())
                    if result or result == 0:
                        if str(result).isnumeric():
                            #delete old variabels
                            erasable = []
                            for tup in block_dict:
                                if tup[1] == "variabel" or tup[1] == "variabeldefinition":
                                    erasable.append(tup)
                            for e_tup in erasable:
                                del block_dict[e_tup]

                            item = self.data_accessor.get_item(result)
                            code_block = get_blocks_from_string(item[0], block_dict)
                            initialization_code_block = get_blocks_from_string(item[1], block_dict)
                            start_block = StartBlock()
                            initialization_block = InitializationBlock()
                            if code_block:
                                start_block.append(code_block)
                            if initialization_code_block:
                                initialization_block.append(initialization_code_block)
                            start_block.update_scale_factor(self.scale_factor)
                            initialization_block.update_scale_factor(self.scale_factor)
                            self.code_block_list = [start_block, initialization_block]
                            
                            self.selector.build()
                        self.wait_for_selection = False
            elif event.type == MOUSEWHEEL:
                self.selection_input.scroll(event.y)
        else:
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_position = pygame.mouse.get_pos()
                    #check if we pressed save
                    if self.menu.is_mouse_on_save():
                        self.wait_for_input = True
                    elif self.menu.is_mouse_on_load():
                        self.wait_for_selection = True
                        self.selection_input.load(self.data_accessor.get_all_items())#give it the names and ids
                    else:
                        #check if we got a new Block by colliding
                        selector_collision = self.selector.check_collision(pygame.Vector2(mouse_position))
                        if selector_collision:
                            if isinstance(selector_collision, Block):#add to the block list
                                if not isinstance(selector_collision, VariabelDefinitionBlock):
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
                    
                    #check for new possible connections and deletion
                    for code_block1 in self.code_block_list:
                        if code_block1.in_focus:
                            if self.menu.is_mouse_on_delete():#try do delete the block in focus
                                if not (isinstance(code_block1, StartBlock) or isinstance(code_block1, InitializationBlock)):
                                    self.code_block_list.remove(code_block1)
                                    break
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
                self.selector.give_keyboard_down_event(event)

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
        if not self.wait_for_input and not self.wait_for_selection:
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

            self.menu.update()
        

    def draw(self, screen):
        #draw background
        screen.fill((255,255,255))
        for code_block in self.code_block_list:
            code_block.draw(screen)
        self.selector.draw(screen)

        self.menu.draw(screen)
        
        if self.wait_for_input:
            self.text_input.draw(screen)

        if self.wait_for_selection:
            self.selection_input.draw(screen)