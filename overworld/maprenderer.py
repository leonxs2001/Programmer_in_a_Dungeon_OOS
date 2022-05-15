from typing import List
import pygame

class MapRenderer(pygame.sprite.Sprite):
    
    def __init__(self,assets,done_map:List):
            pygame.sprite.Sprite.__init__(self)
            self.done_map = done_map
            self.uni_size = (40,40)
            self.outer_wall = pygame.transform.scale(pygame.image.load(assets['outer_wall']),self.uni_size)
            self.ground = pygame.transform.scale(pygame.image.load(assets['gorund']),self.uni_size)
            self.wall = pygame.transform.scale(pygame.image.load(assets['wall']),self.uni_size)
            #print(self.wall.get_rect().size,self.ground.get_rect().size,self.player.get_rect().size)
            print(self.done_map)
            #self.end = pygame.image.load(assets['end'])

    def draw(self, screen : pygame.Surface):
        #screen.blit(self.wall,self.wall_rect.x +60)self.wall_rect
        for x in range(len(self.done_map)):
            for y in range(len(self.done_map[x])):
                if (self.done_map[x][y])[0] == 'outer_wall':
                    screen.blit(self.outer_wall,(self.done_map[x][y])[1])
                elif (self.done_map[x][y])[0] == 'wall':
                    screen.blit(self.wall,(self.done_map[x][y])[1])
                elif (self.done_map[x][y])[0] == 'ground':
                    screen.blit(self.ground,(self.done_map[x][y])[1])
                # elif (self.done_map[x][y])[0] == 'player':
                #     screen.blit(self.ground,(self.done_map[x][y])[1])
                elif (self.done_map[x][y])[0] == 'end':
                    screen.blit(self.ground,(self.done_map[x][y])[1])
                else:
                    screen.blit(self.ground,(self.done_map[x][y])[1])
                
