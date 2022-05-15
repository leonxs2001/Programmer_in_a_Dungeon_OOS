from map import Map
from level import Level

import pygame
from overworld.config import asset
from overworld.maprenderer import MapRenderer
#from overworld.entity import Entity

class OverWorld(Level,Map):
    def __init__(self):
        
        Map.__init__(self,asset['level'])
        
        
        # parse the csv and check if input is valid
        # raise error if necessary  
        err = self.parse_level_csv()
        if err is not None:
            raise err
        err = self.check_level()
        if err is not None:
            raise err
        render_map = self.preProcessLevel()
        
        self.maprenderer = MapRenderer(asset,render_map)
        #self.entity = Entity.__init__(self,)
        
        """Entities, Assign Variables etc"""
    def update(self):
        """Update everything important"""
        pass
    def draw(self, screen):
        screen.fill((255,255,255))
        self.maprenderer.draw(screen)
        #self.entity.draw(screen)

        """Draw everything important on the screen."""
    def give_event(self,event):
        """Get the Events and handle them"""
        pass

