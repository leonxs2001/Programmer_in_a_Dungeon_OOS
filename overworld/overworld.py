from typing import List
from level import Level
import pygame,os,random
from overworld.config import asset
from overworld.maprenderer import MapRenderer
from overworld.entity import Entity
from overworld.monster import Mon

def get_level_list()-> List:
    return random.sample({f.path for f in os.scandir(os.getcwd()+'/overworld/assets/levels')},5)

class OverWorld(Level):

    def __init__(self):
        maps = get_level_list()
        self.maprenderer = MapRenderer(asset,maps)
        self.load_map()

    def load_map(self):
        self.entity = Entity(asset,self.maprenderer.done_map)
        self.monster = Mon(asset, self.maprenderer.done_map)       
        
        """Entities, Assign Variables etc"""
    def update(self):
        """Update everything important"""
        pass
    def draw(self, screen):
        self.maprenderer.draw(screen)
        self.entity.draw(screen)
        self.monster.draw(screen)

        """Draw everything important on the screen."""
    def give_event(self,event):
        """Get the Events and handle them"""
        if event.type == pygame.KEYDOWN:
            self.entity.move(event, self.maprenderer.walls)
            self.maprenderer.checkend(self.entity.playergroup)
            
            
