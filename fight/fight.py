from isort import code
import pygame
import random
from pygame.locals import *
from fight.player.shootingplayer import ShootingPlayer
from fight.player.touchingplayer import TouchingPlayer
from selectioninput import SelectionInput
from sqlitedataaccess import SqliteDataAccess
from overworld.config import asset
from fight.menu import Menu
from level import Level

class Fight(Level):
    def __init__(self):
        #Entities
        self.wait_for_selection = True
        self.data_accessor = SqliteDataAccess()
        self.player = ShootingPlayer("","", False)
        self.opponent = ShootingPlayer("","", True)
        self.player.opponent = self.opponent
        self.opponent.opponent = self.player
        bg_case = pygame.image.load(asset["ground"])
        bg_case = pygame.transform.scale(bg_case, (40, 40))
        self.bg = pygame.Surface((1280, 720))
        for x in range(0, 1281, 40):
            for y in range(0, 721, 40):
                self.bg.blit(bg_case, (x, y))
        
        self.menu = Menu()
        self.last_time = pygame.time.get_ticks()

    def reset(self, opponent_type):
        
        self.menu.wait = True
        self.last_time = pygame.time.get_ticks()
        
        self.wait_for_selection = True
        self.selection_input = SelectionInput("Choose your code:")
        self.selection_input.load(self.data_accessor.get_all_items())

        op_type = opponent_type[0]
        op_strength = opponent_type[1]#use strength later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        codes = self.data_accessor.get_all_items(True, op_type)#get all codes
        choosen_one = random.randint(0, len(codes) - 1)
        item_id = codes[choosen_one][1]
        item_code = self.data_accessor.get_item(item_id)

        opponent_damage = 10
        if op_strength > 1:
            opponent_damage = 15

        if op_type == "s":#is shooting player
            self.opponent = ShootingPlayer(item_code[1], item_code[0], True, opponent_damage)
        else:#is melee
            self.opponent = TouchingPlayer(item_code[1], item_code[0], True, opponent_damage)

    def update(self):
        if not self.wait_for_selection:
            #calculate elapsed time
            new_time = pygame.time.get_ticks()
            elapsed_time = new_time - self.last_time
            self.last_time = new_time

            self.menu.update()
            if not self.menu.wait:
                self.player.update(elapsed_time)
                self.opponent.update(elapsed_time)
                #check collsion between the two players
                if self.player.rect.colliderect(self.opponent.rect):
                    self.player.process_collision(elapsed_time)
                    self.opponent.process_collision(elapsed_time)

                if self.player.life_controller.lifes <= 0:
                    return False
                elif self.opponent.life_controller.lifes <= 0:
                    return True

    def give_event(self, event):
        if self.wait_for_selection:
            if event.type == MOUSEWHEEL:
                self.selection_input.scroll(event.y)
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    result = self.selection_input.check_collision(pygame.mouse.get_pos())
                    if result or result == 0:
                        if not str(result).isnumeric():
                            result = 1
                        item = self.data_accessor.get_item(result)
                        self.player = ShootingPlayer(item[1], item[0], False)
                        self.player.opponent = self.opponent
                        self.opponent.opponent = self.player

                        self.wait_for_selection = False
        else:
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_SPACE:
                    if self.player.ready:
                        self.player.next_step()
                elif event.key == K_RETURN:
                    self.menu.wait = not self.menu.wait
            elif event.type == MOUSEBUTTONDOWN:
                if self.menu.is_mouse_on_play():
                    self.menu.wait = not self.menu.wait

    def draw(self,screen):
        #Redisplay
        screen.blit(self.bg, (0,0))
        self.player.draw(screen)
        self.opponent.draw(screen)
        self.menu.draw(screen)

        if self.wait_for_selection:
            self.selection_input.draw(screen)
    
    