from typing import List, Tuple
import pygame

class Entity(pygame.sprite.Sprite):
    
    def __init__(self,assets,pos:List):
            pygame.sprite.Sprite.__init__(self)
            self.uni_size = (64,64)
            self.player = pygame.transform.scale(pygame.image.load(assets['player']),self.uni_size)

    def draw(self, screen : pygame.Surface):
        #screen.blit(self.wall,self.wall_rect.x +60)self.wall_rect
        for x in range(len(self.done_map)):
            for y in range(len(self.done_map[x])):
                if (self.done_map[x][y])[0] == 'outer_wall':
                    screen.blit(self.outer_wall,(self.done_map[x][y])[1])
