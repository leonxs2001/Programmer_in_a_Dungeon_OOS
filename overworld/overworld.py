from typing import List
from level import Level
import pygame,os,random
from overworld.config import asset
from overworld.maprenderer import MapRenderer
from overworld.entity import Entity
from overworld.enemy import Mon
from overworld.menu import Menu
from overworld.gameoverscreen import GameOverScreen
from fight.fight import Fight
from codeview.codeview import CodeView


def get_level_list()-> List:
    return random.sample({f.path for f in os.scandir(os.getcwd()+'/overworld/assets/levels')},5)

class OverWorld(Level):
    def __init__(self):
        self.state = 0 # state 0 overworld; 1 fight; 2 codeview; 3 gameover
        self.fight = Fight()
        self.code = CodeView()
        self.menu = Menu()
        self.game_over = GameOverScreen()
        maps = get_level_list()
        self.maprenderer = MapRenderer(asset,maps)
        self.load_map()
        self.last_time = pygame.time.get_ticks()
        self.time = 0

    def load_map(self):
        """Entities, Assign Variables etc"""
        self.entity = Entity(asset,self.maprenderer.done_map)
        self.monster = Mon(asset, self.maprenderer.done_map)  
        
    def update(self):
        """Update everything important"""
        if self.state == 0:   
            fight_tup = self.monster.update(self.maprenderer.walls, self.entity.playergroup)

            if fight_tup != None:
                self.fight.reset(fight_tup)
                self.state = 1
            new_time = pygame.time.get_ticks()
            elapsed_time = new_time - self.last_time
            self.last_time = new_time
            self.time += elapsed_time
            
            self.menu.update()
        elif self.state == 1:
            self.fight.update()
        elif self.state == 2:
            self.code.update()
        

    def draw(self, screen):
        """Draw everything important on the screen."""
        if self.state == 0 or self.state == 3:
            self.maprenderer.draw(screen)
            self.entity.draw(screen)
            self.monster.draw(screen)
            self.menu.draw(screen)
            self.draw_time_text(screen)
            if self.state == 3:
                self.game_over.draw(screen)
        elif self.state == 1:
            self.fight.draw(screen)
        elif self.state == 2:
            self.code.draw(screen)
        #self.entity.draw(screen)

    def give_event(self,event):
        """Get the Events and handle them"""
        if self.state == 0:
            if event.type == pygame.KEYDOWN:
                self.entity.move(event, self.maprenderer.walls)
                if self.maprenderer.checkend(self.entity.playergroup):
                    if self.maprenderer.map_index == 4:
                        self.state = 3
                    else:
                        self.maprenderer.done_map = self.maprenderer.get_map()
                        self.maprenderer.render()
                        self.load_map()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.is_mouse_on_code():
                    self.code.reset()
                    self.state = 2
        elif self.state == 1:
            result = self.fight.give_event(event)
            if result != None:
                if result:
                    pass
                else:
                    self.maprenderer.render()
                    self.load_map()
                    
                    
                self.state = 0
        elif self.state == 2:
            if self.code.give_event(event):
                self.state = 0
        elif self.state == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over.check_collision(pygame.mouse.get_pos()):
                    pygame.quit()

    def draw_time_text(self, screen):
        seconds = int(self.time // 1000)
        time_font = pygame.font.Font(None, 30)
        
        text_color = (93, 217, 72)

        minutes = int(seconds // 60)
        seconds -= 60 * minutes

        seconds = str(seconds)
        minutes = str(minutes)
        if len(seconds) == 1:
            seconds = "0" + seconds
        
        if len(minutes) == 1:
            minutes = "0" + minutes

        time_text = time_font.render(f"Time: {minutes}:{seconds}",True, text_color)
        time_rect = time_text.get_rect()
        time_rect.right = 1260
        time_rect.top = 20
        screen.blit(time_text, time_rect)
