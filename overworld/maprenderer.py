
from typing import List, Tuple
import pygame

class Outerwall(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['outer_wall']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos

class Wall(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['wall']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos
class Ground(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['ground']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos
class End(pygame.sprite.Sprite):
        def __init__(self,assets,size,pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(assets['end']),size)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos



class MapRenderer(pygame.sprite.Sprite):
    
    def __init__(self,assets,done_map:List):
            pygame.sprite.Sprite.__init__(self)
            self.done_map = done_map
            self.uni_size = (40,40)
            self.sprites = pygame.sprite.Group()
            test = Outerwall(assets,self.uni_size,(0,0))
            self.sprites.add(test)
            print(test)
            for x in range(len(self.done_map)):
                for y in range(len(self.done_map[x])):
                    if (self.done_map[x][y])[0] == 'outer_wall':
                        temp = Outerwall(assets,self.uni_size,((self.done_map[x][y])[1]))
                        self.sprites.add(temp)
                    elif (self.done_map[x][y])[0] == 'wall':
                        temp = Wall(assets,self.uni_size,((self.done_map[x][y])[1]))
                        self.sprites.add(temp) 
                    elif (self.done_map[x][y])[0] == 'ground':
                        temp = Ground(assets,self.uni_size,((self.done_map[x][y])[1]))
                        self.sprites.add(temp) 
                    elif (self.done_map[x][y])[0] == 'end':
                        temp = End(assets,self.uni_size,((self.done_map[x][y])[1]))
                        self.sprites.add(temp)
                    else:
                        temp = Ground(assets,self.uni_size,((self.done_map[x][y])[1]))
                        self.sprites.add(temp) 

    def draw(self, screen : pygame.Surface):
        self.sprites.draw(screen)
                
